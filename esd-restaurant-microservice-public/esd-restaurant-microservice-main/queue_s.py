import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

import db_creds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'dbURL') or 'mysql+mysqlconnector://' + db_creds.username + ':' + db_creds.password + '@' + db_creds.hostname + ':3306/ESD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class QueueS(db.Model):
    __tablename__ = 'queue'
    
    queueID = db.Column(db.Integer, nullable = False, primary_key=True)
    phoneNum = db.Column(db.String(8), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    numPax = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(45), nullable = False, default= "Waiting for turn")
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # constructor
    def __init__(self, phoneNum, name, numPax):
        self.phoneNum = phoneNum
        self.name = name
        self.numPax = numPax
    
    def json(self):
        return {"queueID": self.queueID, "phoneNum": self.phoneNum, "name": self.name,  "numPax": self.numPax, "status" : self.status, "date": self.date}
    
# more app.route
@app.route("/queue_s/generateQueue" , methods=['POST'])
def generateQueue():

    # Convert JSON string into JSON object
    data = json.loads(request.get_json())

    # Initialize QueueS class
    newQueue = QueueS(
        phoneNum = data['numInput'], 
        numPax = data['paxInput'], 
        name = data['nameInput']
        )
    print("---- Connected to Queue -----")
    try:
        db.session.add(newQueue)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while generating queue. " + str(e)
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": newQueue.json()
        }
    ), 201
     
@app.route("/queue_s/nextQueue", methods=['PUT'])
def updateNextPerson():
    print('\n\n-----Invoking updateNextPerson service -----')
    queueList = QueueS.query.filter(QueueS.status != "Notified").first()
    
    if queueList: 
        try: 
            # update the status to 'Notified' 
            queueList.status = "Notified" 
            # commit the changes 
            db.session.commit()
        
        # error handling 
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating the queue. " + str(e)
                }
            ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": queueList.json()
        }
    ), 201 
        
@app.route("/queue_s/retrieveAllRecords") 
def retrieveAllRecords(): 
    queueRecords = QueueS.query.all()
    if len(queueRecords):
        return jsonify(
            {
                "code" : 200, 
                "data" : {
                    'records' : [record.json() for record in queueRecords ]
                }
            }
        )

# Alternate way to run flask app
# main
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)

