# 1. Retrieve menu items from menu.py [GET]
# 2. Place order (Send order to info to order.py) [POST]

from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS

import os, sys
from os import environ

import json
import stripe
import amqp_setup
import pika
import requests
from invokes import invoke_http
from datetime import date

stripe.api_key = "sk_test_51Kjn22BTDCs0lLNqkoQkTlZsigzoCrxw0UgViRuZDwRDEEHHCuWk8bUIEIWQvDG99jYAcZ7STaXTmwPZY7QgE5Cu006fbPzGe9"
app = Flask(__name__)
CORS(app)

# menu_URL = "http://localhost:5000/menu"
order_URL = environ.get('order_URL') or "http://localhost:5001/order"
payment_URL = environ.get('payment_URL') or "http://localhost:4242"
updateOrder_URL = 'http://localhost:5001/order'
# getTotalBill_URL = "http://localhost:5001/order/getPaymentAmt_v2"

# global variable
global_bill_obj_list = None
global_totalAmt = 0 

@app.route("/placeOrder", methods=['POST'])
def placeOrder():
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # Send order info to be sent to order.py
            result = processOrder(order)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_an_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processOrder(order_details):
    # Send the order info to order.py
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL, method='POST', json=order_details)
    print('order_result:', order_result)

    code = order_result["code"]
    if code not in range(200, 300):
        # Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Failure in creating order."
        }

    return {
        "code": 201,
        "data": {
            "order_result": order_result,
        }
    }

@app.route("/getTotalBill", methods=['POST'])
def getTotalBill():
    print("Request:", request)
    if request.is_json:
        try:
            queueID = request.get_json()["queueID"]
            print("queueID:", queueID)
            getTotalBill_URL = order_URL + "/getPaymentAmt_v2/"

            getTotalBill_URL += str(queueID)
            # result = invoke_http(getTotalBill_URL, method='POST', json=queueID)
            result = invoke_http(getTotalBill_URL, method='GET')
            print("Result:", result)
            code = result["code"]
            if code not in range(200, 300):

                # Return error
                return {
                    "code": 404,
                    "data": result,
                    "message": "There are no orders for that queueID."
                }

            print(result)
            
            return jsonify(result), code

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_an_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/sendEmail", methods=["POST"])
def sendEmail():
    amqp_setup.check_setup()
    if request.is_json:
        try:
            data = request.get_json()
            userEmail = data["userEmail"]
            totalAmt = data["totalAmt"]
            bill_obj_list = data["bill_obj_list"]
            
            print('--checking bill_obj_list type--')
            print((bill_obj_list))

            # dd/mm/YY
            todayDate = date.today().strftime("%d/%m/%Y")
            print(todayDate)
            email_data = {
                "userEmail": userEmail,
                "totalAmt": totalAmt,
                "bill_obj_list": bill_obj_list,
                "date": todayDate
            }
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email_invoice", 
            body=json.dumps(email_data), properties=pika.BasicProperties(delivery_mode = 2))
          
            return jsonify({
                "code" : 200, 
                "message" : 'Receipt has been sent to your email!'
            })

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_an_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
    
@app.route("/pay", methods=["POST"])
def callStripe():
    queueID = request.form["queueID"]
    
    # Save a copy of the bill_obj_list for the email subsequently
    global global_bill_obj_list  
    global global_totalAmt
    
    global_totalAmt = request.form['totalAmt']
    
    print("queueID:", queueID)
    getTotalBill_URL = order_URL + "/getPaymentAmt_v2/"

    getTotalBill_URL += str(queueID)
    # result = invoke_http(getTotalBill_URL, method='POST', json=queueID)
    
    # this is to interact with the order to retrieve the total bill 
    result = invoke_http(getTotalBill_URL, method='GET')
    totalPrice = result["data"]["totalPrice"]
    # keeping the bill_obj_list for email later 
    global_bill_obj_list = result['data']['items']
    
    # double check if the total amount is correct
    if float(totalPrice) == float(request.form["totalAmt"]):
        # redirect to the payment.py 
        # return redirect(payment_URL + "/create-checkout-session", code=307)
        return redirect(payment_URL, code=307)
    else:
        return jsonify({
                "code": 400,
                "message": "Client supplied total price is incorrect"
            }), 400

@app.route("/paymentSuccess", methods=["GET"])
def payment_success():
    print('--- inside payment_success function ---')
    queueID = request.args.get("queueID")
    session = stripe.checkout.Session.retrieve(request.args.get('sessionID'))
    email = session.customer_details.email
    # Interact with order microservice to update the status 
    url = order_URL + '/' + str(queueID)
    
    print('\n-----order microservice to activate status change-----')
    result = invoke_http(url, method='PUT')

    if result["status"] == "Success" : 
    # Activate the email microservice to email the invoice 
        print('---Proceed to email---')
        jsonObj = {'userEmail': email, 'totalAmt': global_totalAmt, 'bill_obj_list': global_bill_obj_list }
        emailResult = invoke_http('http://localhost:5200/sendEmail', method='POST', json=(jsonObj))
        
        # since email is fire and forget, proceed to just display end page
        # Display a 'Thank you' page to the customer 
        # Insert code to do whatever after payment is successful

        return redirect('http://localhost:8080/UI/thanks.html', code=303)
        # return render_template('test.html')
        
    else : 
        # return back to the homepage and display a payment error. contact stuff 
        return '<h1> There was an error processing your payment. Please inform our staff for further assistance! </h1>'

if __name__ == "__main__":
    # print("This is flask " + os.path.basename(__file__) +
    #       " for placing an order...")
    app.run(host="0.0.0.0", port=5200, debug=True)