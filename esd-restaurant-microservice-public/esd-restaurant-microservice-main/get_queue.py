# flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS

import json 

# amqp imports
import amqp_setup
import pika

import os, sys
from os import environ

# helper function
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

queue_URL = environ.get('queue_URL') or "http://localhost:5003/queue_s/generateQueue"

@app.route("/getQueue", methods=['POST'])
def getQueue():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # converts the JSON object into python data
            queueRequest = request.get_json()
            print("\nReceived an order in JSON:", queueRequest)
            result = processGetQueue(queueRequest)
            
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "get_queue.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processGetQueue(queueRequest):
    # 1. Send the request queue number info 
    # Invoke the queue microservice
    # print('\n-----Invoking queue microservice-----')
    
    # this is to create a new queue
    queue_result = invoke_http(queue_URL, method='POST', json=queueRequest)
    print('queue_result:', queue_result)

    # If generate queue success, invoke notification microservice
    code = queue_result["code"]
    if code in range(200, 300):
        print('\n\n-----Invoking notification.py microservice-----')
        # notification_result = invoke_http(notification_URL, method="POST", json=queue_result['data'])
        queue_result['data']['type'] = 'registration'
        
        # Publish a request to the sms_registration queue
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="sms", 
            body=json.dumps(queue_result['data']), properties=pika.BasicProperties(delivery_mode = 2))
         
         # Disregarding the response of the AMQP, proceed to return the Queue number back to the UI 
        return {
            "code": 201,
            "data": {
                "queue_result": queue_result["data"]
            }
        }
    else: 
        # the queue creation was not successful 
        return queue_result





# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
