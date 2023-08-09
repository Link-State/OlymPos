import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList

def adminLogin(id="", pwd="", store_uid=-1) :
    uid = Admins.findUID(id=id)
    
    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "002"}

    user = Admins.getUser(uid=uid)

    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "003"}
    
    store = StoreInfo.getStore(store_uid)

    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "004"}

    # 매장이 이미 로그인 상태일 때,
    if "isLogin" in store and store["isLogin"] == 1 :
        return {"result" : "Invalid", "code" : "005"}
    
    # 로그인 상태로 변경
    StoreInfo.setIsLogin(uid=store_uid, islogin=1)

    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000"
    }

def userLogin(id="", pwd="", store_uid=-1, tableNum=-1) :
    uid = Admins.findUID(id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "002"}

    user = Admins.getUser(uid)
    
    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "003"}
    
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "004"}
    
    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)

    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : "006"}

    # 해당 테이블 번호가 이미 로그인 상태인지 확인할 것.
    if "isLogin" in table and table["isLogin"] == 1 :
        return {"result" : "Invalid", "code" : "005"}
    
    # 테이블 로그인 상태로 변경
    TableList.setIsLogin(store_uid=store_uid, tableNum=tableNum, islogin=1)

    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000"
    }

def adminLogout(id="", pwd="", tableNum=-1) :
    if (id == "asdf" and pwd == "1234") :
        return {"result" : "Success"}
    else :
        return {"result" : "Invalid"}

def userLogout(id="", pwd="", tableNum=-1) :

    if (id == "asdf" and pwd == "1234") :
        return {"result" : "Success"}
    else :
        return {"result" : "Invalid"}

def signup() :
    return

def delete_account() :
    return