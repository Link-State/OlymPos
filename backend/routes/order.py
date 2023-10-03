import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from statusCode import *
from flask import request, jsonify, session
from flask_jwt_extended import *
from flask_restful import Resource
from controllers import order

class Product_order(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(order.product_order(inputData=user_data))
    
class Change_order_state(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        if identity is None :
            return jsonify({"return" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(order.change_order_state(inputData=user_data))

class Change_table_state(Resource) :
    @jwt_required()
    def post(self) :
        return

class Get_order_list(Resource) :
    @jwt_required()
    def get(self) :
        return

class Get_table_list(Resource) :
    @jwt_required()
    def get(self) :
        return