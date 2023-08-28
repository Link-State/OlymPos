import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList
from models import Product

def checkField(data) :
    keyword = []

    if "name" in data :
        if len(data["name"]) < MinLength.store_name and len(data["name"]) > MaxLength.store_name :
            keyword.append("name")

    if "owner" in data :
        if len(data["owner"]) < MinLength.store_owner and len(data["owner"]) > MaxLength.store_owner :
            keyword.append("owner")

    if "address" in data :
        if len(data["address"]) < MinLength.store_address and len(data["address"]) > MaxLength.store_address :
            keyword.append("address")

    if "tel_num" in data :
        if len(data["tel_num"]) < MinLength.store_tel_number and len(data["tel_num"]) > MaxLength.store_tel_number :
            keyword.append("tel_num")

    return keyword

def addStore(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    fields = ["user_id", "name", "owner", "address", "tel_num", "count"]
    for field in fields :
        if field not in inputStoreInfo :
            return {"result" : "Invalid", "code" : "100"}

    uid = Admins.findUID(id=inputStoreInfo["user_id"])

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "200"}

    store_uid = StoreInfo.findStore(uid=uid, name=inputStoreInfo["name"])

    # 이미 해당 유저에게 존재하는 매장일 때,
    if store_uid != -1 :
        store = StoreInfo.getStore(uid=store_uid)
        
        # 삭제된 매장일 때,
        if store["disable_date"] != None :
            return {"result" : "Invalid", "code" : "102"}
        
        return {"result" : "Invalid", "code" : "300"}
    
    keyword = checkField(inputStoreInfo)

    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : "301", "keyword" : keyword}
    
    inputStoreInfo["unique_admin"] = uid

    # DB에 매장 추가
    StoreInfo.add(inputStoreInfo)

    store_uid = StoreInfo.findStore(uid=uid, name=inputStoreInfo["name"])

    # 매장 추가가 안됐을 때,
    if store_uid == -1 :
        return {"result" : "Invalid", "code" : "103"}

    # 테이블을 1부터 순차적으로 추가
    for table in range(1, inputStoreInfo["count"]+1) :
        TableList.add(store_uid=store_uid, tableNum=table)

    return {"result" : "Success", "code" : "005", "uid" : store_uid}