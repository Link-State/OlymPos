import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList
from models import Product

def adminLogin(id="", pwd="", store_uid=-1) :
    uid = Admins.findUID(id=id)
    
    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    user = Admins.getUser(uid=uid)

    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "201"}
    
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "202"}
    
    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000"
    }

def userLogin(id="", pwd="") :
    uid = Admins.findUID(id=id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    user = Admins.getUser(uid=uid)
    
    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "201"}
    
    # 매장 목록 검색
    stores = StoreInfo.getStores(admin_uid=uid)

    return {
        "result" : "Success",
        "code" : "000",
        "stores" : stores
    }

def tableLogin(ssaid="", store_uid=-1, tableNum = -1) :
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "202"}
    
    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)

    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : "203"}

    # 해당 테이블 번호가 이미 로그인 상태인지 확인할 것.
    if "isLogin" in table and table["isLogin"] != '' :
        return {"result" : "Invalid", "code" : "204"}
    
    # 테이블 로그인 상태로 변경
    TableList.setIsLogin(store_uid=store_uid, tableNum=tableNum, islogin=ssaid)

    products = Product.getProducts(store_uid=store_uid)

    return {
        "result" : "Success",
        "code" : "000",
        "products" : products
    }

def adminLogout(id="") :
    uid = Admins.findUID(id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}
    
    return {"result" : "Success", "code" : "001"}

def userLogout(ssaid="", store_uid=-1, tableNum=-1) :
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "202"}

    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)

    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : "203"}

    # 로그인 상태가 아닐 때,
    if "isLogin" in table and table["isLogin"] == '' :
        return {"result" : "Invalid", "code" : "205"}
    
    # SSAID가 맞지 않을 때,
    if table["isLogin"] != ssaid :
        return {"result" : "Invalid", "code" : "204"}
    
    # 로그아웃
    TableList.setIsLogin(store_uid=store_uid, tableNum=tableNum, islogin='')
    
    return {"result" : "Success", "code" : "001"}

def signup(member={}) :
    
    # 필수 값이 누락 됐을 때,
    if "id" not in member or "pwd" not in member or "name" not in member or "phone" not in member or "email" not in member :
        return {"result" : "Invalid", "code" : "100"}
    
    # 이미 존재하는 아이디일때,
    uid = Admins.findUID(id=member["id"])
    if uid != -1 :
        return {"result" : "Invalid", "code" : "206"}
    
    # DB에 회원 추가
    Admins.add(member)
    
    return {"result" : "Success", "code" : "002"}

def delete_account() :
    # isAvailable = 1
    return