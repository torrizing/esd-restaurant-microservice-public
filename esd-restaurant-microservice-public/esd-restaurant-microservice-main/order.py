#!/usr/bin/python3

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_cors import CORS

from datetime import datetime
import json
from os import environ
import db_creds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://' + db_creds.username + ':' + db_creds.password + '@' + db_creds.hostname + ':3306/ESD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Order(db.Model):
    __tablename__ = 'order'

    orderID = db.Column(db.Integer, primary_key=True)
    queueID = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'orderID': self.orderID,
            'queueID': self.queueID,
            'status': self.status,
            'created': self.created,
            'modified': self.modified
        }

        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json())

        return dto

class Menu(db.Model):
    __tablename__ = 'menu'

    itemID = db.Column(db.String(5), primary_key=True)
    itemName = db.Column(db.String(100), nullable=False)
    itemPrice = db.Column(db.Float(precision=2), nullable=False)
    itemImageUrl = db.Column(db.String(100))
    available = db.Column(db.Boolean, nullable=False)

    def __init__(self, itemID, itemName, itemPrice, itemImageUrl, available):
        self.itemID = itemID
        self.itemName = itemName
        self.itemPrice = itemPrice
        self.itemImageUrl = itemImageUrl
        self.available = available

    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "price": self.itemPrice, "itemImageUrl": self.itemImageUrl, "available": self.available}

class Order_Item(db.Model):
    __tablename__ = 'order_item'

    itemID = db.Column(db.ForeignKey(
        'menu.itemID', ondelete='CASCADE', onupdate='CASCADE'), index=True, primary_key=True)
    orderID = db.Column(db.ForeignKey(
        'order.orderID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, itemID, quantity):
        self.itemID = itemID
        self.quantity = quantity

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    order = db.relationship(
        'Order', primaryjoin='Order_Item.orderID == Order.orderID', backref='order_item')

    def json(self):
        return {'itemID': self.itemID, 'quantity': self.quantity, 'orderID': self.orderID}

@app.route("/order")
def get_all():
    orderlist = Order.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404

@app.route("/order/<int:order_id>")
def find_by_order_id(order_id):
    order = Order.query.filter_by(orderID=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404

@app.route("/order", methods=['POST'])
def create_order():
    print("order POST line 129", request.get_json())
    queueID = request.json.get('queueID', None)
    order = Order(queueID=queueID, status='Unpaid')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            itemID=item['itemID'], quantity=item['quantity']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500
    
    print(json.dumps(order.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201

@app.route("/order/<int:queue_id>", methods=['PUT'])
def update_order(queue_id):
    try:
        orders = Order.query.filter_by(queueID=queue_id)
        if not orders:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "queueID": queue_id
                    },
                    "message": "This queue ID does not have any orders."
                }
            ), 404
        
        for order in orders: 
            order.status = 'Paid'
            db.session.commit()
            print(db.session.commit())
            
        return jsonify(
            {
                "code": 200,
                "status" : 'Success'
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "status" : "An error occurred while updating the order status"
            }
        ), 500

# @app.route("/order/getPaymentAmt/<int:queue_id>")
# def getAmountPayable(queue_id):
#     stmt = text(
#                 "SELECT SUM(total_price) "
#                 "FROM ("
#                 "SELECT ESD.order.orderID, queueID, order_item.itemID, menu.itemPrice, order_item.quantity, order_item.quantity * itemPrice AS total_price "
#                 "FROM ESD.order, ESD.order_item , ESD.menu "
#                 "WHERE menu.itemID = order_item.itemID AND order_item.orderID = ESD.order.orderID AND queueID = :queueID "
#                 ") as table1 "
#                 "GROUP BY table1.queueID")
#     stmt = stmt.bindparams(queueID = queue_id)
#     result = db.session.execute(stmt).fetchone()
#     if result:
#         return jsonify(
#             {
#                 "code": 200,
#                 "amountPayable": round(result[0], 2)
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "queue_id": queue_id
#             },
#             "message": "Order not found for specified queue_id."
#         }
#     ), 404

@app.route("/order/getPaymentAmt_v2/<int:queue_id>")
def getAmountPayable2(queue_id):
    stmt = text("select order_item.orderID, ESD.order.queueID, menu.itemID, menu.itemName, itemPrice, SUM(order_item.quantity) as total_qty from order_item, ESD.order, menu"
                " where order_item.itemID = menu.itemID and order_item.orderID = ESD.order.orderID and queueID = :queueID and ESD.order.status = 'Unpaid'"
                " group by order_item.itemID"
                )
    stmt = stmt.bindparams(queueID = queue_id)
    result = db.session.execute(stmt)
    print("order.py Results:", result)
    print("order.py Results dict:", result == None)
    if result:
        row_as_dict = []
        total_price = 0
        for row in result:
            row_as_dict.append(dict(row))
            total_price += row[4] * float(row[5])

        if len(row_as_dict) == 0:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "queue_id": queue_id
                    },
                    "message": "Order not found for specified queue_id."
                }
            ), 404

        return jsonify(
            {
                "code": 200,
                "data" : {
                    "items" : row_as_dict,
                    "totalPrice" : round(total_price, 2)
                }
            }
        )
    

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5001, debug=True)