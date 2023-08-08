import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import request, jsonify, session
from flask_jwt_extended import *
from flask_restful import Resource
from controllers import account

class AdminLogin(Resource) :
    def post(self) :
        id = ""
        pwd = ""
        user_data = request.get_json()

        if "id" in user_data and "pwd" in user_data :
            id = user_data["id"]
            pwd = user_data["pwd"]
        
        # 세션에 토큰 저장
        return jsonify(account.adminLogin(id=id, pwd=pwd))
    
class UserLogin(Resource) :
    def post(self) :
        user_data = request.get_json()
        id = ""
        pwd = ""
        tableNum = -1

        if "id" in user_data and "pwd" in user_data :
            id = user_data["id"]
            pwd = user_data["pwd"]
        if "tableNum" in user_data :
            tableNum = user_data["tableNum"]
        
        # 세션에 토큰 저장
        return jsonify(account.login(id, pwd, tableNum))

class AdminLogout(Resource) :
    @jwt_required()
    def post(self) :
        #identity = user_id
        identity = get_jwt_identity()
        if identity is None :
            return "Invalid"
        
class UserLogout(Resource) :
    @jwt_required()
    def post(self) :
        #identity = user_id
        identity = get_jwt_identity()
        if identity is None :
            return "Invalid"
        

class Signup(Resource) :
    def post(self) :
        return "signup"


class Delete_account(Resource) :
    def post(self) :
        return "delete account"


class Change_account_info(Resource) :
    def post(self) :
        return "change_account_info"

