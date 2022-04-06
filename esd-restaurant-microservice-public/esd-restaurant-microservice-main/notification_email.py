from flask import Flask, request, jsonify
from flask_cors import CORS

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
    
    queue_name = 'email_invoice'
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
def callback(channel, method, properties, body): # required signature for the callback; no return
    print('activated inside callback!')
    sendEmailInvoice(body)


def sendEmailInvoice(body):
    print('\n\n-----Invoking sendEmailInvoice service from Simple -----')
    body = json.loads(body)
    print(body)

    userEmail = body["userEmail"]
    totalAmt = body["totalAmt"]
    items = body["bill_obj_list"]
    date = body["date"]
    
    print(items)
    
    # Start
    receiptTemplate = f"""
    <html>
    <h2> Here are your transactional details. </h2>
    """
    
    
    # Body
    receiptTemplate += f"""
        <table border='1'>
            <tr>
                    <th style="width:100px">Item Code</th>
                    <th style="width:100px">Item Name</th>
                    <th style="width:100px">Item Price ($)</th>
                    <th style="width:100px">Quantity</th>
                    <th style="width:100px">Total ($)</th>
                </tr>
    """
    
    for item in items:
        receiptTemplate += f"""
            <tr>
                <td style="text-align:center">{item['itemID']}</td>  
                <td style="text-align:center">{item['itemName']}</td>  
                <td style="text-align:center">{item['itemPrice']}</td>  
                <td style="text-align:center">{ item['total_qty'] }</td> 
                <td style="text-align:center">{round(( float(item['itemPrice']) * int(item['total_qty'])),2)}</td> 
            </tr>
        """
    
    # End
    receiptTemplate += f"""
             <tr>
                    <td colspan="4" style="text-align: right;">Total Payable:</td>
                    <td style="text-align:center"> {totalAmt} </td>   
            </tr>
            </table>
            <h2> Thank you for visiting Eight Sushi on {date}! </h2>
            </html>
            
        """
        
    # Replace with own API Key
    apiKey = ""                    
    return requests.post("https://api.mailgun.net/v3/sandbox6a80d089d38a492999c27b95c3fbf9ca.mailgun.org/messages", 
        auth=("api", apiKey), 
        data={
        "from": "Eight Sushi <eightSushi@sushiGood.com>",
        "to": userEmail,
        "subject":"Here is your e-Receipt!",
        "html": receiptTemplate
        })    
   

if __name__ == '__main__':
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveMessageLog()