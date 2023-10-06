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
    if "product_name" in data :
        if len(data["product_name"]) < MinLength.product_name or len(data["product_name"]) > MaxLength.product_name :
            keyword.append("product_name")
    if "option_name" in data :
        if len(data["option_name"]) < MinLength.option_name or len(data["option_name"]) > MaxLength.option_name :
            keyword.append("option_name")
    if "suboption_name" in data :
        if len(data["suboption_name"]) < MinLength.suboption_name or len(data["suboption_name"]) > MaxLength.suboption_name :
            keyword.append("suboption_name")

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

def add_option(inputData={}) :
    fields = ["store_uid", "option_name", "price", "isoffer"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=inputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}

    option_uid = ProductOption.findOption(store_uid=inputData["store_uid"], name=inputData["option_name"], price=inputData["price"], isoffer=inputData["isoffer"])
    
    # 해당 이름+가격+서브옵션유무의 옵션이 이미 존재할 때,
    if option_uid == -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}

    keyword = checkField(inputData)
    
    # 데이터 양식이 맞지 않을 때,
    if len(keyword) <= 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # 옵션 생성
    uid = ProductOption.add(inputData)
    return {"result" : "Success", "code" : Code.Success, "uid" : uid}

def modify_option(inputData={}) :
    fields = ["option_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.getOption(uid=inputData["option_uid"])

    # 해당 옵션이 존재하지 않을 때,
    if len(option) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}
    
    store = StoreInfo.getStore(uid=option["unique_store_info"])
    user = Admins.getUser(store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    keyword = checkField(inputData)

    # 데이터 형식이 올바르지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    option_uid = ProductOption.findOption(name=inputData["option_name"], price=inputData["price"], isoffer=inputData["isoffer"])

    # 해당 이름+가격+서브옵션유무의 옵션이 이미 존재할 때,
    if option_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}

    # 옵션 수정
    if "option_name" in inputData :
        ProductOption.setName(uid=inputData["option_uid"], name=inputData["option_name"])
    if "price" in inputData :
        ProductOption.setPrice(uid=inputData["option_uid"], price=inputData["price"])
    if "isoffer" in inputData :
        ProductOption.setIsOffer(uid=inputData["option_uid"], isoffer=inputData["isoffer"])

    # 버전 업데이트
    Version.setProductOption(uid=option["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def delete_option(inputData={}) :
    fields = ["option_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.getOption(uid=inputData["option_uid"])

    # 해당 옵션이 존재하지 않을 때,
    if len(option) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}
    
    store = StoreInfo.getStore(uid=option["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 옵션 삭제
    ProductOption.remove(uid=inputData["option_uid"])

    # 버전 업데이트
    Version.setProductOption(uid=option["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def add_suboption(inputData={}) :
    fields = ["option_uid", "suboption_name", "price", "amount"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.getOption(uid=inputData["option_uid"])

    # 옵션이 존재하지 않을 때,
    if len(option) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}
    
    store = StoreInfo.getStore(uid=option["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    keyword = checkField(inputData)

    # 데이터 형식이 맞지 않은 경우
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # 이름+가격+남은수량 서브옵션이 이미 존재할 때,
    
    # 서브옵션 생성
    uid = ProductSuboption.add(inputData)

    return {"result" : "Success", "code" : Code.Success, "uid" : uid}

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
