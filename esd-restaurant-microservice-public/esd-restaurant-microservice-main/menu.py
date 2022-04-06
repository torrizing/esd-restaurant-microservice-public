#!/usr/bin/python3

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


class Menu(db.Model):
    __tablename__ = 'menu'

    itemID = db.Column(db.String(5), primary_key=True)
    itemName = db.Column(db.String(100), nullable=False)
    itemPrice = db.Column(db.Float(precision=2), nullable=False)
    itemImageUrl = db.Column(db.String(200))
    available = db.Column(db.Boolean, nullable=False)

    def __init__(self, itemID, itemName, itemPrice, itemImageUrl, available):
        self.itemID = itemID
        self.itemName = itemName
        self.itemPrice = itemPrice
        self.itemImageUrl = itemImageUrl
        self.available = available

    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "price": self.itemPrice, "itemImageUrl": self.itemImageUrl, "available": self.available}


@app.route("/menu", methods=['GET'])
def get_all():
    menu = Menu.query.all()
    if len(menu):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "menuItems": [item.json() for item in menu]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items."
        }
    )
    
@app.route("/menu/createNewItem", methods=['POST'])
def createNewItem():
    print('---inside createNewItem---')
    
    # Convert JSON string into JSON object
    data = json.loads(request.get_json())
    print("Create new menu items:", data)
    # to verify if itemID is unique
    if (Menu.query.filter_by(itemID=data['itemID']).first()):
        return jsonify(
            {
                "code": 400,
                "message": "ItemID already exists. Please pick a unique ID."
            }
        ), 400 
    
    if data['available'] == 'true' :
        availability = True 
    else : 
        availability = False 
    
    # Initialize Menu class
    newMenu = Menu(
        itemID = data['itemID'],
        itemName = data['itemName'],
        itemPrice = data['itemPrice'],
        itemImageUrl = data['itemImageUrl'],
        available = availability,
    )
    
    # print(newMenu)
    
    print("---- Connected to Menu Database -----")
    try:
        db.session.add(newMenu)
        db.session.commit()
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating a new item. " + str(e)
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "message": 'Successfully added a new item to the menu!'
        }
    ), 201

@app.route("/menu/deleteItem", methods=['POST'])
def deleteItem():
    print('---inside deleteItem---')
    
    # Convert JSON string into JSON object
    data = json.loads(request.get_json())
    
    print(data)    
    
    item = Menu.query.filter_by(itemID=data['itemID']).first()
    
    if item: 
        db.session.delete(item)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message" : 'Item deleted successfully!'
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Failed to delete item! Please try again!"
        }
    ), 404
    
@app.route("/menu/editItems", methods=["PUT"])
def editItem(): 
    print('---inside editItem---')
    
    # Convert JSON string into JSON object
    data = json.loads(request.get_json())
    print("Edit menu item:", data)
    
    item = Menu.query.filter_by(itemID=data['editItemID']).first()
    
    print('from here!')
    print(data['availability'])
    
    
    if data['availability'] == True or data['availability'] == 'true':
        availability = True 
    else : 
        availability = False 
    
    print('in here!')
    print(availability)
    
    if item: 
        # update all 
        item.itemName = data["editItemName"]
        item.itemPrice = data["editPrice"]
        item.itemImageUrl = data["editImageURL"]
        item.available = availability
        db.session.commit()
        return jsonify( 
            {
                "code": 200,
                "data": item.json(),
                "message": "Successfully updated!"
            }          
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "Failed to update! Please try again!"
        }
    )
    

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
