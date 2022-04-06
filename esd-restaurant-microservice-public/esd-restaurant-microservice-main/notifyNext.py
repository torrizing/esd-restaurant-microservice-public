# complex microservice that will orchestrate 
# a) Notification microservice 
# b) Queue microservice 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json 

# amqp imports
import amqp_setup
import pika

import os, sys
from os import environ

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

notifyNextPerson_URL = environ.get('notifyNextPerson_URL') or "http://localhost:5003/queue_s/nextQueue"
retrieveAllRecords_URL = environ.get('retrieveAllRecords_URL') or "http://localhost:5003/queue_s/retrieveAllRecords"

# Description: Calls for notifyNextPerson to retrieve the customer details 
# Trigger notification 
@app.route("/notifyNext")
def notifyNext():
    print('\n\n-----Invoking notifyNextPerson microservice-----')
    try : 
        result = processNotificationNext()
        return jsonify(result) 
    
    except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "notifyNext.py internal error: " + ex_str
            }), 500 
        

def processNotificationNext():
    print('\n\n-----Invoking processNotificationNext function -----')
    # Suppose to call for nextQueue microservice that will return the details of the first person (that has not been notified). 
    
    nextPersonDetails = invoke_http(notifyNextPerson_URL, method='PUT')

    print(nextPersonDetails)
    
    code = nextPersonDetails["code"]
    data = nextPersonDetails["data"]
    
    # The details then be passed to Twilio API to send SMS for reminder 
    if code in range(200,300) : 
        # Invoke notification service 
        print('\n\n-----Invoking notifyCustomer microservice through Complex -----')
        # outcome = invoke_http(notifyCustomer_URL, method='POST', json = data)
        data['type'] = 'notifyNext'
        
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="sms", 
        body=json.dumps(data), properties=pika.BasicProperties(delivery_mode = 2)) 
        
        return {
                "code" : 200, 
                "data" : 'Customer has been informed!'
            }
    else: 
        return {
            "code" : 401, 
            "data" : 'Unsuccessful!'
        }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)