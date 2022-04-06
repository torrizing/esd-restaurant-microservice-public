from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from twilio.rest import Client
import amqp_setup
import json

import os
import requests


app = Flask(__name__)
CORS(app)

monitorBindingKey='#'

def receiveMessageLog():
    print('---triggering receiveMessageLog---')
    amqp_setup.check_setup()
    
    queue_name = 'sms'
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
def callback(channel, method, properties, body): # required signature for the callback; no return
    print('activated inside callback!')
    notifyCustomer(body)


def notifyCustomer(body):
    print('\n\n-----Invoking displayCustQueueNo service from Simple -----')
    body = json.loads(body)
    
    # Your Account SID from twilio.com/console
    # Your Auth Token from twilio.com/console
    yourAccSID = ""
    yourAuthToken = ""

    account_sid = yourAccSID
    auth_token  = yourAuthToken
    client = Client(account_sid, auth_token)
    
    name = body['name']
    contactNumber = '+65' + str(body['phoneNum'])
    queueNo = body['queueID']
    

    if(body['type'] == 'registration') :
        queueNo = body['queueID']
        numPax = body['numPax']
       
        message = client.messages.create(
            to = contactNumber, 
            from_ = "+17315033203",
            body = f"Dear {name},\nyour Q number {queueNo} for table of {numPax} has been confirmed. Thank you.")

        print(message.status)
    
    elif (body['type'] == 'notifyNext') : 
        
        url = f"http://localhost:5501/UI/menu.html?queueID={queueNo}"
      
        message = client.messages.create(
            to= contactNumber, 
            from_="+17315033203",
            body= f"Hello {name}, Your queue number has been called! Please come to the restaurant. Please use the following link to access our restaurant's menu! Link: {url} ")

        print(message.status)
        

if __name__ == '__main__':
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveMessageLog()