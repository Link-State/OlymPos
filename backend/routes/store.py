import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import request, jsonify, session
from flask_jwt_extended import *
from flask_restful import Resource
from controllers import store

class AddStore(Resource) :
    @jwt_required()
    def post(self) :
        identity = get_jwt_identity()

        # 토큰이 없을 경우
        if identity is None :
            return jsonify({"result" : "Invalid", "code" : "101"})
        
        user_data = request.get_json()
        user_data["user_id"] = identity

        return jsonify(store.addStore(inputStoreInfo=user_data))