import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import request, jsonify
from flask_jwt_extended import *
from flask_restful import Resource
from utils import *
from statusCode import *
from controllers import product

class Add_group(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})

        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.add_group(user_data))

class Modify_group(Resource) :
    @jwt_required()
    
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.modify_group(user_data))

class Delete_group(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.delete_group(inputData=user_data))

# ajax로 json과 image 동시에 전송
# https://celdan.tistory.com/42

class Add_product(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})

        user_data = request.get_json()

        user_data["user_id"] = identity

        return jsonify(product.add_product(userData=user_data))
    
class Modify_product(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()

        user_data["user_id"] = identity
        
        return jsonify(product.modify_product(userData=user_data))
    
class Delete_product(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.delete_product(userData=user_data))
    
class Add_option(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.add_option(inputData=user_data))
    
class Modify_option(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.modify_option(inputData=user_data))
    
class Delete_option(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.delete_option(inputData=user_data))
    
class Add_suboption(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.add_suboption(inputData=user_data))
    
class Modify_suboption(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.modify_suboption(inputData=user_data))
    
class Delete_suboption(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.delete_suboption(inputData=user_data))

class Modify_product_option_relation(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()
        
        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(product.modify_product_option_relation(inputData=user_data))

class Get_group_list(Resource) :
    @jwt_required()
    def get(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.args.to_dict()
        user_data["user_id"] = identity

        return jsonify(product.get_group_list(inputData=user_data))

class Get_product_list(Resource) :
    @jwt_required()
    def get(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.args.to_dict()
        user_data["user_id"] = identity

        return jsonify(product.get_product_list(inputData=user_data))
    
class Get_option_list(Resource) :
    @jwt_required()
    def get(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : Code.MissingToken})
        
        user_data = request.args.to_dict()
        user_data["user_id"] = identity

        return jsonify(product.get_option_list(inputData=user_data))