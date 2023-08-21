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
        store_uid = ""
        user_data = request.get_json()

        if "id" not in user_data or "pwd" not in user_data or "store_uid" not in user_data :
            return jsonify({"result" : "Invalid", "code" : "001"})
        
        id = user_data["id"]
        pwd = user_data["pwd"]
        store_uid = user_data["store_uid"]
        result = account.adminLogin(id=id, pwd=pwd, store_uid=store_uid)

        # 세션에 토큰 저장
        return jsonify(result)
    
class UserLogin(Resource) :
    def post(self) :
        user_data = request.get_json()
        id = ""
        pwd = ""

        # 필수 값이 누락 됐을 때,
        if "id" not in user_data or "pwd" not in user_data :
            return jsonify({"result" : "Invalid", "code" : "100"})
        
        id = user_data["id"]
        pwd = user_data["pwd"]
        
        return jsonify(account.userLogin(id=id, pwd=pwd))

class TableLogin(Resource) :
    def post(self) :
        user_data = request.get_json()
        ssaid = ""
        store_uid = -1
        table_num = -1

        # 필수 값이 누락 됐을 때,
        if "SSAID" not in user_data or "store_uid" not in user_data or "table" not in user_data :
            return jsonify({"result" : "Invalid", "code" : "100"})
        
        ssaid = user_data["SSAID"]
        store_uid = user_data["store_uid"]
        table_num = user_data["table"]

        return jsonify(account.tableLogin(ssaid=ssaid, store_uid=store_uid, tableNum=table_num))

class AdminLogout(Resource) :
    @jwt_required()
    def post(self) :
        #identity = user_id
        identity = get_jwt_identity()
        if identity is None :
            return "Invalid"
        
class UserLogout(Resource) :
    def post(self) :
        user_data = request.get_json()
        ssaid = ""
        store_uid = -1
        table = -1

        # 필수 값이 누락 됐을 때,
        if "SSAID" not in user_data or "store_uid" not in user_data or "table" not in user_data :
            return jsonify({"result" : "Invalid", "code" : "100"})
        
        ssaid = user_data["SSAID"]
        store_uid = user_data["store_uid"]
        table = user_data["table"]

        return jsonify(account.userLogout(ssaid=ssaid, store_uid=store_uid, tableNum=table))

class Signup(Resource) :
    def post(self) :
        return "signup"


class Delete_account(Resource) :
    def post(self) :
        return "delete account"


class Change_account_info(Resource) :
    def post(self) :
        return "change_account_info"

