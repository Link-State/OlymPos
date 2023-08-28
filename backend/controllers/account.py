import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList
from models import Product

def get_account(id=-1) :
    uid = Admins.findUID(id=id)
    
    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    user = Admins.getUser(uid=uid)

    user["user_pwd"] = "BLINDED"

    return user

def adminLogin(id="", pwd="") :
    uid = Admins.findUID(id=id)
    
    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    user = Admins.getUser(uid=uid)
    
    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}

    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "201"}
    
    stores = StoreInfo.getStores(admin_uid=uid)

    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000",
        "stores" : stores
    }

def userLogin(id="", pwd="") :
    uid = Admins.findUID(id=id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    user = Admins.getUser(uid=uid)
    
    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}
    
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
    
    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}

    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)

    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : "203"}
    
    # 삭제된 테이블일 때,
    if table["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}

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
    
    user = Admins.getUser(uid=uid)

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}
    
    return {"result" : "Success", "code" : "001"}

def userLogout(ssaid="", store_uid=-1, tableNum=-1) :
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : "202"}
    
    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}
    
    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)
    
    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : "203"}
    
    # 삭제된 매장일 때,
    if table["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}

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
    if "user_id" not in member or "user_pwd" not in member or "name" not in member or "phone" not in member or "email" not in member :
        return {"result" : "Invalid", "code" : "100"}

    uid = Admins.findUID(id=member["user_id"])

    # 존재하지 않는 아이디일 때,
    if uid == -1 :
        # DB에 회원 추가
        Admins.add(member)

        return {"result" : "Success", "code" : "002"}
    
    user = Admins.getUser(uid=uid)

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}
    
    # 이미 존재하는 아이디일 때,
    return {"result" : "Invalid", "code" : "206"}

def delete_account(id='') :
    uid = Admins.findUID(id=id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}
    
    user = Admins.getUser(uid=uid)

    # 이미 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}

    Admins.remove(uid=uid)

    return {"result" : "Success", "code" : "004"}

def change_account(member={}) :
    uid = Admins.findUID(id=member["user_id"])

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}
    
    user = Admins.getUser(uid=uid)

    # 이미 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : "102"}
    
    keyword = []

    # 형식 체크
    ## 비밀번호 검사
    if "before_pwd" in member and "after_pwd" in member :
        if member["before_pwd"] != user["user_pwd"] :
            return {"result" : "Invalid", "code" : "201"}
        if len(member["after_pwd"]) > Length.user_pwd :
            keyword.append("user_pwd")

    ## 이름 검사
    if "name" in member :
        if len(member["name"]) > Length.user_name :
            keyword.append("user_name")

    ## 전화번호 검사
    if "phone" in member :
        if len(member["phone"]) > Length.phone_number :
            # 문자열 길이, 하이픈 등 조건 검사
            keyword.append("phone_number")

    ## 이메일 검사
    if "email" in member :
        memberLength = len(member["email"])
        alphaIdx = member["email"].find('@')
        dotIdx = member["email"].find('.')
        if memberLength > Length.email or alphaIdx <= 1 or dotIdx <= 3 or dotIdx - alphaIdx <= 1 or dotIdx+1 == memberLength :
            keyword.append("email")

    # 양식이 맞지 않은 정보가 존재할 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : "207", "keyword" : keyword}
    
    # 정보 수정
    ## 비밀번호 수정
    if "before_pwd" in member and "after_pwd" in member :
        Admins.setPWD(uid=uid, pwd=member["after_pwd"])

    ## 이름 수정
    if "name" in member :
        Admins.setName(uid=uid, name=member["name"])

    ## 전화번호 수정
    if "phone" in member :
        Admins.setPhoneNum(uid=uid, num=member["phone"])

    ## 이메일 수정
    if "email" in member :
        Admins.setEmail(uid=uid, email=member["email"])

    return {"result" : "Success", "code" : "003", "keyword" : keyword}