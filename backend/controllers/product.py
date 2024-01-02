import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from statusCode import *
from flask_jwt_extended import *
from datetime import datetime
from models.mysql import DB
from models.Admins import Admins
from models.StoreInfo import StoreInfo
from models.TableList import TableList
from models.ProductGroup import ProductGroup
from models.Product import Product
from models.ProductOption import ProductOption
from models.ProductOptionRelations import ProductOptionRelations
from models.ProductSuboption import ProductSuboption
from models.OrderList import OrderList
from models.SelectedOption import SelectedOption
from models.Version import Version

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
    
    store = StoreInfo.query.get(userInputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.filter_by(user_id=userInputData["user_id"]).first()

    # 유저가 존재하지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    # 해당 매장이 요청자 소유가 아닐 때,
    if user.unique_admin != store.unique_admin :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    product_group = ProductGroup.query.filter_by(
        unique_store_info=userInputData["store_uid"],
        group_name=userInputData["group_name"]
    ).first()
    
    # 해당 이름의 그룹이 이미 존재할 때,
    if product_group != None :
        return {"result" : "Invalid", "code" : Code.AlreadyExistGroup}
    
    keyword = checkField(userInputData)

    # 데이터 형식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 카테고리 생성
    product_group = ProductGroup(
        store=userInputData["store_uid"],
        name=userInputData["group_name"]
    )
    DB.session.add(product_group)

    # 버전 업데이트
    version = Version.query.get(store.unique_store_info)
    
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version.product_group = now_lnt

    DB.session.commit()
    
    return {"result" : "Success", "code" : Code.Success, "uid" : product_group.unique_product_group}

def modify_group(userInputData) :
    fields = ["group_uid", "group_name"]

    # 필수 필드가 누락 됐을 때,
    for field in fields :
        if field not in userInputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    user = Admins.query.filter_by(user_id=userInputData["user_id"]).first()

    # 유저가 존재하지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    group = ProductGroup.query.get(userInputData["group_uid"])

    # 정보를 수정하려는 그룹이 존재하지 않을 때,
    if group == None :
        return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    groups = ProductGroup.query.filter_by(unique_store_info=group.unique_store_info, group_name=userInputData["group_name"])

    # 해당 이름의 그룹이 이미 매장에 존재할 때,
    if groups.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistGroup}
    
    keyword = checkField(userInputData)

    # 데이터 형식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # 그룹 정보 수정
    group.group_name = userInputData["group_name"]

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(group.unique_store_info)
    version.product_group = now_lnt

    DB.session.commit()

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
    if option_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}

    keyword = checkField(inputData)
    
    # 데이터 양식이 맞지 않을 때,
    if len(keyword) > 0 :
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
    
    if "option_name" in inputData :
        option["option_name"] = inputData["option_name"]
    if "price" in inputData :
        option["price"] = inputData["price"]
    if "isoffer" in inputData :
        option["suboption_offer"] = inputData["isoffer"]

    option_uid = ProductOption.findOption(store_uid=store["unique_store_info"], name=option["option_name"], price=option["price"], isoffer=option["suboption_offer"])

    # 해당 이름+가격+서브옵션유무의 옵션이 이미 존재할 때,
    if option_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}
    
    update_count = 0

    # 옵션 수정
    if "option_name" in inputData :
        ProductOption.setName(uid=inputData["option_uid"], name=inputData["option_name"])
        update_count += 1
    if "price" in inputData :
        ProductOption.setPrice(uid=inputData["option_uid"], price=inputData["price"])
        update_count += 1
    if "isoffer" in inputData :
        ProductOption.setIsOffer(uid=inputData["option_uid"], isoffer=inputData["isoffer"])
        update_count += 1

    # 버전 업데이트
    if update_count > 0 :
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

    suboption_uid = ProductSuboption.findSubOption(name=inputData["suboption_name"], price=inputData["price"], amount=inputData["amount"])

    # 이름+가격+남은수량 서브옵션이 이미 존재할 때,
    if suboption_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistSubOption}
    
    # 서브옵션 생성
    uid = ProductSuboption.add(inputData)

    return {"result" : "Success", "code" : Code.Success, "uid" : uid}

def modify_suboption(inputData={}) :
    fields = ["suboption_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    suboption = ProductSuboption.getSubOption(uid=inputData["suboption_uid"])

    # 해당 서브옵션이 존재하지 않을 때,
    if len(suboption) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}
    
    option = ProductOption.getOption(uid=suboption["unique_product_option"])
    store = StoreInfo.getStore(uid=option["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    keyword = checkField(inputData)
    
    # 바꾸려는 옵션이 존재하지 않을 때, (데이터 형식이 맞지 않을 때,)
    if "option_uid" in inputData :
        option = ProductOption.getOption(uid=inputData["option_uid"])
        if len(option) <= 0 :
            keyword.append("option_uid")
    
    # 데이터 형식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 변경 데이터 적용
    if "suboption_name" in inputData :
        suboption["suboption_name"] = inputData["suboption_name"]
    if "price" in inputData :
        suboption["price"] = inputData["price"]
    if "amount" in inputData :
        suboption["amount"] = inputData["amount"]

    suboption_uid = ProductSuboption.findSubOption(name=suboption["suboption_name"], price=suboption["price"], amount=suboption["amount"])

    # 중복 데이터가 존재할 때,
    if suboption_uid != -1 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistSubOption}
    
    update_count = 0

    # 서브옵션 수정
    if "option_uid" in inputData :
        ProductSuboption.setOption(uid=inputData["suboption_uid"], option_id=inputData["option_uid"])
        update_count += 1
    if "suboption_name" in inputData :
        ProductSuboption.setName(uid=inputData["suboption_uid"], name=inputData["suboption_name"])
        update_count += 1
    if "price" in inputData :
        ProductSuboption.setPrice(uid=inputData["suboption_uid"], price=inputData["price"])
        update_count += 1
    if "amount" in inputData :
        ProductSuboption.setAmount(uid=inputData["suboption_uid"], amount=inputData["amount"])
        update_count += 1

    # 버전 업데이트
    if update_count > 0 :
        Version.setProductSuboption(uid=store["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def delete_suboption(inputData={}) :
    fields = ["suboption_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    suboption = ProductSuboption.getSubOption(uid=inputData["suboption_uid"])

    # 서브옵션이 존재하지 않을 때,
    if len(suboption) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}
    
    option = ProductOption.getOption(uid=suboption["unique_product_option"])
    store = StoreInfo.getStore(uid=option["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 서브옵션 삭제
    ProductSuboption.remove(uid=inputData["suboption_uid"])

    # 버전 업데이트
    Version.setProductSuboption(uid=store["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def modify_product_option_relation(inputData={}) :
    fields = ["product_uid", "option_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 데이터 형식이 맞지 않을 때,
    if type(inputData["option_uid"]) is not type(list()) :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : ["option_uid"]}

    product = Product.getProduct(uid=inputData["product_uid"])

    # 존재하지 않는 상품일 때,
    if len(product) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProduct}
    
    store = StoreInfo.getStore(uid=product["unique_store_info"])
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    relations = ProductOptionRelations.getOptions(product_uid=inputData["product_uid"])

    create = list(set(inputData["option_uid"]).difference(set(relations)))
    delete = list(set(relations).difference(set(inputData["option_uid"])))
    
    not_exist_options = []

    # 존재하지 않는 옵션이 하나라도 있을 때,
    for uid in create :
        option = ProductOption.getOption(uid=uid)

        if len(option) <= 0 :
            not_exist_options.append(uid)

    if len(not_exist_options) > 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption, "keyword" : not_exist_options}

    # 상품-옵션 관계 수정
    # 1. 삭제
    for option_uid in delete :
        ProductOptionRelations.remove(product_uid=inputData["product_uid"], option_uid=option_uid)
    
    # 2. 생성
    for option_uid in create :
        ProductOptionRelations.add(product_uid=inputData["product_uid"], option_uid=option_uid)

    # 버전 업데이트
    Version.setProductOptionRelations(uid=store["unique_store_info"])

    return {"result" : "Success", "code" : Code.Success}

def get_group_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.getStore(uid=inputData["store_uid"])
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    groups = ProductGroup.getGroups(store_uid=inputData["store_uid"])

    return {"result" : "Success", "code" : Code.Success, "groups" : groups}

def get_product_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.getStore(uid=inputData["store_uid"])
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    products = Product.getProducts(store_uid=inputData["store_uid"])

    return {"result" : "Success", "code" : Code.Success, "products" : products}

def get_option_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.getStore(uid=inputData["store_uid"])
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.getUser(uid=store["unique_admin"])

    # 요청자와 소유자가 일치하지 않을 때,
    if inputData["user_id"] != user["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    options = ProductOption.getOptions(store_uid=inputData["store_uid"])

    return {"result" : "Success", "code" : Code.Success, "options" : options}
