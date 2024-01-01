import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from statusCode import *
from flask_jwt_extended import *
from models.Admins import Admins
from models.StoreInfo import StoreInfo
from models import TableList
from models import Product
from models import mysql

def checkField(data) :
    keyword = []

    if "user_id" in data :
        if len(data["user_id"]) < MinLength.user_id or len(data["user_id"]) > MaxLength.user_id :
            keyword.append("user_id")

    if "after_pwd" in data :
        if len(data["after_pwd"]) < MinLength.user_pwd or len(data["after_pwd"]) > MaxLength.user_pwd :
            keyword.append("after_pwd")
    
    if "user_pwd" in data :
        if len(data["user_pwd"]) < MinLength.user_pwd or len(data["user_pwd"]) > MaxLength.user_pwd :
            keyword.append("user_pwd")

    if "name" in data :
        if len(data["name"]) < MinLength.user_name or len(data["name"]) > MaxLength.user_name :
            keyword.append("name")

    if "phone" in data :
        if len(data["phone"]) < MinLength.phone_number or len(data["phone"]) > MaxLength.phone_number :
            keyword.append("phone")

    if "email" in data :
        memberLength = len(data["email"])
        alphaIdx = data["email"].find('@')
        dotIdx = data["email"].find('.')
        if memberLength < MinLength.email or memberLength > MaxLength.email or alphaIdx <= 1 or dotIdx <= 3 or dotIdx - alphaIdx <= 1 or dotIdx+1 == memberLength :
            keyword.append("email")
        
    return keyword

def get_account(id=-1) :
    uid = Admins.findUID(id=id)
    
    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    user = Admins.getUser(uid=uid)

    user["user_pwd"] = "BLINDED"

    return {"result" : "Success", "code" : Code.Success, "user" : user}

def adminLogin(id="", pwd="") :
    user = Admins.query.filter_by(user_id=id, user_pwd=pwd).first()
    
    # 해당 아이디/비밀번호의 계정이 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = user.__dict__

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    rows = StoreInfo.query.filter_by(unique_admin=user["unique_admin"]).all()

    stores = []
    for row in rows :
        store = dict()
        store["unique_admin"] = row.unique_admin
        store["store_name"] = row.store_name
        store["store_owner"] = row.store_owner
        store["store_tel_number"] = row.store_tel_number
        store["table_count"] = row.table_count
        store["disable_date"] = row.disable_date
        stores.append(store)

    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : Code.Success,
        "stores" : stores
    }

def userLogin(id="", pwd="") :
    uid = Admins.findUID(id=id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    user = Admins.getUser(uid=uid)
    
    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : Code.WrongPWD}
    
    # 매장 목록 검색
    stores = StoreInfo.getStores(admin_uid=uid)

    return {"result" : "Success", "code" : Code.Success, "stores" : stores}

def tableLogin(ssaid="", store_uid=-1, tableNum = -1) :
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)

    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistTable}
    
    # 삭제된 테이블일 때,
    if table["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    # 해당 테이블 번호가 이미 로그인 상태인지 확인할 것.
    if "isLogin" in table and table["isLogin"] != '' :
        return {"result" : "Invalid", "code" : Code.AlreadyLogin, "SSAID" : table["isLogin"]}
    
    # 테이블 로그인 상태로 변경
    TableList.setIsLogin(store_uid=store_uid, tableNum=tableNum, islogin=ssaid)

    products = Product.getProducts(store_uid=store_uid)

    return {"result" : "Success", "code" : Code.Success, "products" : products}

def adminLogout(id="") :
    uid = Admins.findUID(id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = Admins.getUser(uid=uid)

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    return {"result" : "Success", "code" : Code.Success}

def userLogout(ssaid="", store_uid=-1, tableNum=-1) :
    store = StoreInfo.getStore(store_uid)
    
    # 매장이 검색되지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    table = TableList.getTable(store_uid=store_uid, tableNum=tableNum)
    
    # 테이블이 검색되지 않을 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistTable}

    # 로그인 상태가 아닐 때,
    if "isLogin" in table and table["isLogin"] == '' :
        return {"result" : "Invalid", "code" : Code.NotLoginState}
    
    # 요청자와 로그인중인 사용자의 SSAID가 일치하지 않을 때,
    if table["isLogin"] != ssaid :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 로그아웃
    TableList.setIsLogin(store_uid=store_uid, tableNum=tableNum, islogin='')
    
    return {"result" : "Success", "code" : Code.Success}

def signup(inputUserData={}) :
    
    fields = ["user_id", "user_pwd", "name", "phone", "email"]

    # 필수 값이 누락 됐을 때,
    for field in fields :
        if field not in inputUserData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    uid = Admins.findUID(id=inputUserData["user_id"])

    # 이미 존재하는 아이디일 때,
    if uid != -1 :
        user = Admins.getUser(uid=uid)

        # 탈퇴한 유저라면,
        if user["disable_date"] != None :
            return {"result" : "Invalid", "code" : Code.DeletedData}
        
        return {"result" : "Invalid", "code" : Code.AlreadyExistID}
    
    # user = Admins.findUID(EMAIL)
    # 이미 존재하는 이메일일 때,
    result = mysql.get(table="Admins", cols=["unique_admin"], conds=[f"""email = '{inputUserData["email"]}'"""])
    
    if len(result) > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadyEmail}

    # 이메일 인증 기능
    

    keyword = checkField(inputUserData)

    # 입력 필드 확인
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # DB에 회원 추가
    Admins.add(inputUserData)

    return {"result" : "Success", "code" : Code.Success}

def delete_account(id='') :
    uid = Admins.findUID(id=id)

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = Admins.getUser(uid=uid)

    # 이미 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    Admins.remove(uid=uid)

    return {"result" : "Success", "code" : Code.Success}

def change_account(inputUserData={}) :
    uid = Admins.findUID(id=inputUserData["user_id"])

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = Admins.getUser(uid=uid)

    # 이미 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 비밀번호 변경 시 기존 비밀번호 일치 확인
    if "before_pwd" in inputUserData and "after_pwd" in inputUserData and inputUserData["before_pwd"] != user["user_pwd"] :
        return {"result" : "Invalid", "code" : Code.WrongPWD}

    keyword = checkField(inputUserData)

    # 양식이 맞지 않은 정보가 존재할 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 정보 수정
    ## 비밀번호 수정
    if "before_pwd" in inputUserData and "after_pwd" in inputUserData :
        Admins.setPWD(uid=uid, pwd=inputUserData["after_pwd"])

    ## 이름 수정
    if "name" in inputUserData :
        Admins.setName(uid=uid, name=inputUserData["name"])

    ## 전화번호 수정
    if "phone" in inputUserData :
        Admins.setPhoneNum(uid=uid, num=inputUserData["phone"])

    ## 이메일 수정
    if "email" in inputUserData :
        Admins.setEmail(uid=uid, email=inputUserData["email"])

    return {"result" : "Success", "code" : Code.Success, "keyword" : keyword}

def get_isExist(userInputData={}) :

    # 필수 필드가 누락 됐을 때,
    if "user_id" not in userInputData :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    isExist = 0
    uid = Admins.findUID(id=userInputData["user_id"])

    # 해당 아이디를 가진 유저가 이미 존재할 떄,
    if uid != -1 :
        isExist = 1

    return {"result" : "Success", "code" : Code.Success, "isExist" : isExist}

def find_account(inputData={}) :
    # 필수 필드가 누락 됐을 때,
    fields = ['name', 'tel_num', 'email']
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    conds=[f"name = '{inputData['name']}'",
           f"phone_number = '{inputData['tel_num']}'",
           f"email = '{inputData['email']}'"]
    
    user = mysql.get(table="Admins", cols=["unique_admin", "user_id"], conds=conds)

    # 해당 조건으로 비밀번호를 찾을 수 없을 때,
    if len(user) != 1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = user[0]

    return {"result" : "Success", "code" : Code.Success, "user" : user}

def find_password(inputData={}) :
    return