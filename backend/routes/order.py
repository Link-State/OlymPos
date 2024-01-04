import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from statusCode import *
from flask import request, jsonify
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
        identity = get_jwt_identity()

        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(order.change_table_state(inputData=user_data))

class Get_order_list(Resource) :
    @jwt_required()
    def get(self) :
        identity = get_jwt_identity()

        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.args.to_dict()
        user_data["user_id"] = identity

        return jsonify(order.get_order_list(inputData=user_data))

class Get_table_list(Resource) :
    @jwt_required()
    def get(self) :
        identity = get_jwt_identity()

        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.args.to_dict()
        user_data["user_id"] = identity

        return jsonify(order.get_table_list(inputData=user_data))