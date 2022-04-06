import os
from os import environ

import json
import stripe
from flask import Flask, jsonify, redirect, request, render_template

app = Flask(__name__, static_folder='public',
            static_url_path='', template_folder='public')

place_an_order_URL = environ.get('place_an_order_URL') or "http://localhost:5200"

# stripe_keys = {
#     "secret_key": os.environ["STRIPE_SECRET_KEY"],
#     "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
#     "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
# }

# Your stripe api key
yourAPIKey = ""
stripe.api_key = yourAPIKey


# def calculate_order_amount(items):
#     # Replace this constant with a calculation of the order's amount
#     # Calculate the order total on the server to prevent
#     # people from directly manipulating the amount on the client
#     return 1400


# @app.route('/create-payment-intent', methods=['POST'])
# def create_payment():
#     try:
#         # data = json.loads(request.data)
#         # Create a PaymentIntent with the order amount and currency
#         intent = stripe.PaymentIntent.create(
#             # amount=calculate_order_amount(data['items']),
#             amount=500,
#             currency='sgd',
#             automatic_payment_methods={
#                 'enabled': True,
#             },
#         )
#         return jsonify({
#             'clientSecret': intent['client_secret']
#         })
#     except Exception as e:
#         return jsonify(error=str(e)), 403
    
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  totalAmt = request.form["totalAmt"]
  totalAmt = int(float(totalAmt) * 100)
  # creating a Stripe session
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'sgd',
        'product_data': {
          'name': 'Grand Total',
        },
        'unit_amount': totalAmt,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url= place_an_order_URL + "/paymentSuccess?queueID=" + request.form["queueID"] + "&sessionID={CHECKOUT_SESSION_ID}",
    # cancel_url='http://localhost/esd_proj/esd-restaurant-microservice/UI/menu.html?queueID=' + request.form["queueID"],
    cancel_url='http://localhost:8080/UI/menu.html?queueID=' + request.form["queueID"],
  )
  
  return redirect(session.url, code=303)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242, debug=True)
















# YOUR_DOMAIN = 'http://localhost:4242'

# @app.route("/hello")
# def hello_world():
#     print(os.environ)

#     return jsonify("hello world!")

# @app.route("/")
# def index():
#     return render_template("checkout.html")

# @app.route("/config")
# def get_publishable_key():
#     stripe_config = {"publicKey": stripe_keys["publishable_key"]}
#     return jsonify(stripe_config)


# @app.route("/create-checkout-session")
# def create_checkout_session():
#     domain_url = "http://127.0.0.1:5000/"
#     stripe.api_key = stripe_keys["secret_key"]

#     try:
#         # Create new Checkout Session for the order
#         # Other optional params include:
#         # [billing_address_collection] - to display billing address details on the page
#         # [customer] - if you have an existing Stripe Customer ID
#         # [payment_intent_data] - capture the payment later
#         # [customer_email] - prefill the email input in the form
#         # For full details see https://stripe.com/docs/api/checkout/sessions/create

#         # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#         checkout_session = stripe.checkout.Session.create(
#             success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
#             cancel_url=domain_url + "cancelled",
#             payment_method_types=["card"],
#             mode="payment",
#             line_items=[
#                 {
#                     "name": "Tomato",
#                     "quantity": 1,
#                     "currency": "sgd",
#                     "amount": "700",
#                 }
#             ]
#         )
#         return jsonify({"sessionId": checkout_session["id"]})
#     except Exception as e:
#         return jsonify(error=str(e)), 403
        
# @app.route("/success")
# def success():
#     return render_template("success.html")

# @app.route("/cancelled")
# def cancelled():
#     return render_template("cancelled.html")     

# @app.route("/webhook", methods=["POST"])
# def stripe_webhook():
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get("Stripe-Signature")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, stripe_keys["endpoint_secret"]
#         )

#     except ValueError as e:
#         # Invalid payload
#         return "Invalid payload", 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return "Invalid signature", 400

#     # Handle the checkout.session.completed event
#     if event["type"] == "checkout.session.completed":
#         print("Payment was successful.")
#         # TODO: run some custom code here

#     return "Success", 200  

#acct_1Kjn22BTDCs0lLNq


# pk_test_51Kjn22BTDCs0lLNqJ0LGuTs7VDxld89ORW7EZc4CNGf3wwIfsZSFB5mk0IrrcBSH1VsMuK7jZJz49hbZivLg9PPx00GCy9gzPF

# sk_test_51Kjn22BTDCs0lLNqkoQkTlZsigzoCrxw0UgViRuZDwRDEEHHCuWk8bUIEIWQvDG99jYAcZ7STaXTmwPZY7QgE5Cu006fbPzGe9

