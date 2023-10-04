import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from statusCode import *
from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList
from models import ProductGroup
from models import Product
from models import ProductOption
from models import ProductOptionRelations
from models import ProductSuboption
from models import OrderList
from models import SelectedOption
from models import Version

def checkField(data) :
    keyword = []

    if "group_name" in data :
        if len(data["group_name"]) < MinLength.group_name or len(data["group_name"]) > MaxLength.group_name :
            keyword.append("group_name")

    return keyword

def add_group(userInputData={}) :

    fields = ["store_uid", "group_name"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in userInputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=userInputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    uid = Admins.findUID(id=userInputData["user_id"])

    # 유저가 존재하지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    # 해당 매장이 요청자 소유가 아닐 때,
    if store["unique_admin"] != uid :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    group_uid = ProductGroup.findGroup(store_uid=userInputData["store_uid"], name=userInputData["group_name"])
    
    # 해당 이름의 그룹이 이미 존재할 때,
    if group_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistGroup}
    
    keyword = checkField(userInputData)

    # 데이터 형식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 카테고리 생성
    group_uid = ProductGroup.add(userInputData)
    Version.setProductGroup(uid=store["unique_store_info"])
    
    return {"result" : "Success", "code" : Code.Success, "uid" : group_uid}

def modify_group(userInputData) :
    fields = ["group_uid", "group_name"]

    # 필수 필드가 누락 됐을 때,
    for field in fields :
        if field not in userInputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    uid = Admins.findUID(id=userInputData["user_id"])

    # 유저가 존재하지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    group = ProductGroup.getGroup(uid=userInputData["group_uid"])

    # 해당 그룹이 존재하지 않을 때,
    if len(group) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    groups = ProductGroup.getGroups(store_uid=group["unique_store_info"])

    # 해당 이름을 가진 그룹이 이미 존재할 때,
    for g in groups :
        if g["group_name"] == userInputData["group_name"] :
            return {"result" : "Invalid", "code" : Code.AlreadyExistGroup}

    keyword = checkField(userInputData)

    # 데이터 형식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # 그룹 정보 수정
    ProductGroup.setName(uid=userInputData["group_uid"], name=userInputData["group_name"])
    Version.setProductGroup(uid=group["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def delete_group(inputData={}) :
    fields = ["group_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    group = ProductGroup.getGroup(uid=inputData["group_uid"])

    # 해당 카테고리가 존재하지 않을 때,
    if len(group) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    store = StoreInfo.getStore(uid=group["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 해당 매장의 소유주와 요청자의 id가 다를 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 해당 카테고리 삭제
    ProductGroup.remove(uid=inputData["group_uid"])

    # 버전 업데이트
    Version.setProductGroup(uid=group["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def add_product() :
    return

def modify_product() :
    return

def delete_product() :
    return

def add_option() :
    return

def modify_option() :
    return

def delete_option() :
    return

def add_suboption() :
    return

def nodify_suboption() :
    return

def delete_suboption() :
    return

def get_group_list() :
    return

def get_product_list() :
    return

def get_option_list() :
    return
