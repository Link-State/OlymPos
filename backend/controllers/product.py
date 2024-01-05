import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
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
    if "price" in data :
        if data["price"] < 0 :
            keyword.append("price")
    if "amount" in data :
        if data["amount"] < -1 :
            keyword.append("amount")
    if "image" in data :
        exts = [".jpg", ".png"]
        ext =  str(os.path.splitext(data["image"].filename)[1]).lower()
        if ext not in exts :
            keyword.append("image")
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
    
    group = ProductGroup.query.get(inputData["group_uid"])

    # 해당 카테고리가 존재하지 않을 때,
    if group == None :
        return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    store = StoreInfo.query.get(group.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 해당 매장의 소유주와 요청자의 id가 다를 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 해당 카테고리 삭제
    group.disable_date = datetime.now()

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(group.unique_store_info)
    version.product_group = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def add_product(userData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid", "group_uid", "product_name", "price", "amount"]
    for field in fields :
        if field not in userData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
        
    # 매장이 존재하지 않는 경우,
    store = StoreInfo.query.get(userData["store_uid"])

    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    # 상품 그룹이 존재하지 않는 경우
    group = ProductGroup.query.get(userData["group_uid"])

    if group == None :
        return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    # 상품 그룹이 소유자의 매장이 아닌 경우,
    if group.unique_store_info != store.unique_store_info :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    user = Admins.query.get(store.unique_admin)
    
    # 해당 매장이 요청자의 소유가 아닐 경우
    if user.user_id != userData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 데이터 형식 검사
    keywords = checkField(userData)

    ## 데이터 형식이 맞지 않을 때,
    if len(keywords) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keywords" : keywords}
    
    # 해당 상품이 이미 존재할 경우,
    product = Product.query.filter_by(
        unique_store_info=store.unique_store_info,
        unique_product_group=group.unique_product_group,
        product_name=userData["product_name"]
    )

    if product.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadtExistProduct}
    
    # 상품 생성
    product = Product(
        store=store.unique_store_info,
        group=group.unique_product_group,
        name=userData["product_name"],
        price=userData["price"],
        amount=userData["amount"]
    )

    DB.session.add(product)
    DB.session.commit()

    # 상품 사진 불러오기 및 저장
    image = ""
    if "image" in userData :
        image_f = userData["image"]
        ext = os.path.splitext(image_f.filename)[1]
        image = Path.ADMIN + "/" + str(user.unique_admin) + "/store/" + str(store.unique_store_info) + "/product/" + str(product.unique_product) + ext
        image_f.save(image)
    
    # 설명 불러오기
    description = ""
    if "description" in userData :
        description = userData["description"]

    # 사진 및 설명 적용
    product.image = image
    product.description = description
    
    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success, "uid" : product.unique_product}

def modify_product(userData={}) :
    fields = ["product_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in userData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    product = Product.query.get(userData["product_uid"])

    # 해당 상품이 존재하지 않을 경우,
    if product == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    store = StoreInfo.query.get(product.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않는 경우,
    if user.user_id != userData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}

    # (key가 있는 경우) 그룹이 존재하지 않는 경우,
    group = None
    if "group_uid" in userData :
        group = ProductGroup.query.get(userData["group_uid"])

        if group == None :
            return {"result" : "Invalid", "code" : Code.NotExistGroup}
    
    # 수정하려는 그룹이 소유자의 매장이 아닌 경우,
    if group.unique_store_info != store.unique_store_info :
        return {"result" : "Invalid", "code" : Code.NotEquals}

    # 데이터 양식 검사
    keywords = checkField(userData)

    if len(keywords) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keywords" : keywords}
    
    # 기존 상품 정보
    unique_product_group = product.unique_product_group
    product_name = product.product_name
    price = product.price
    image = product.image
    description = product.description
    amount = product.amount

    # 기존 상품 정보에 수정하고자 하는 정보 덮어씌우기
    if "group_uid" in userData :
        unique_product_group = userData["group_uid"]
    if "product_name" in userData :
        product_name = userData["product_name"]
    if "price" in userData :
        price = userData["price"]
    if "description" in userData :
        description = userData["description"]
    if "amount" in userData :
        amount = userData["amount"]

    # 상품 중복 검사
    modify_product = Product.query.filter_by(
        unique_store_info=store.unique_store_info,
        unique_product_group=unique_product_group,
        product_name=product_name
    )

    if modify_product.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadtExistProduct}
    
    # 이미지의 경우 덮어씌우기
    if "image" in userData :
        # 기존 이미지 삭제
        if os.path.isfile(product.image) :
            os.remove(product.image)

        # 새 이미지 저장
        image_f = userData["image"]
        ext = os.path.splitext(image_f.filename)[1]
        image = Path.ADMIN + "/" + str(user.unique_admin) + "/store/" + str(store.unique_store_info) + "/product/" + str(product.unique_product) + ext
        image_f.save(image)

    # 수정된 정보 적용
    product.unique_product_group = unique_product_group
    product.product_name = product_name
    product.price = price
    product.image = image
    product.description = description
    product.amount = amount

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product = now_lnt
    
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def delete_product(userData={}) :
    fields = ["product_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in userData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    # 해당 상품이 존재하지 않을 때,
    product = Product.query.get(userData["product_uid"])
    
    if product == None :
        return {"result" : "Invalid", "code" : Code.NotExistProduct}

    # 요청자와 상품의 소유자가 일치하지 않을 때,
    store = StoreInfo.query.get(product.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    if user.user_id != userData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 해당 상품 삭제
    product.disable_date = datetime.now()

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def add_option(inputData={}) :
    fields = ["store_uid", "option_name", "price", "isoffer"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.query.get(inputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}

    option = ProductOption.query.filter_by(
        unique_store_info=inputData["store_uid"],
        option_name=inputData["option_name"],
        price=inputData["price"],
        suboption_offer=inputData["isoffer"]
    ).first()

    # 해당 이름+가격+서브옵션유무의 옵션이 이미 존재할 때,
    if option != None :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}

    keyword = checkField(inputData)
    
    # 데이터 양식이 맞지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # 옵션 생성
    option = ProductOption(
        store=inputData["store_uid"],
        name=inputData["option_name"],
        price=inputData["price"],
        offer=inputData["isoffer"]
    )

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(inputData["store_uid"])
    version.product_option = now_lnt

    DB.session.add(option)
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success, "uid" : option.unique_product_option}

def modify_option(inputData={}) :
    fields = ["option_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.query.get(inputData["option_uid"])

    # 해당 옵션이 존재하지 않을 때,
    if option == None :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}

    store = StoreInfo.query.get(option.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    keyword = checkField(inputData)

    # 데이터 형식이 올바르지 않을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 옵션 수정
    option_name = option.option_name
    price = option.price
    suboption_offer = option.suboption_offer

    if "option_name" in inputData :
        option_name = inputData["option_name"]
    if "price" in inputData :
        price = inputData["price"]
    if "isoffer" in inputData :
        suboption_offer = inputData["isoffer"]

    modify_option = ProductOption.query.filter_by(
        unique_store_info=store.unique_store_info,
        option_name=option_name,
        price=price,
        suboption_offer=suboption_offer
    )

    # 해당 이름+가격+서브옵션유무의 옵션이 이미 존재할 때,
    if modify_option.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistOption}

    option.option_name = option_name
    option.price = price
    option.suboption_offer = suboption_offer

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(option.unique_store_info)
    version.product_option = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def delete_option(inputData={}) :
    fields = ["option_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.query.get(inputData["option_uid"])

    # 해당 옵션이 존재하지 않을 때,
    if option == None :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}

    store = StoreInfo.query.get(option.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 옵션 삭제
    option.disable_date = datetime.now()

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(option.unique_store_info)
    version.product_option = now_lnt

    DB.session.commit()
    return {"result" : "Success", "code" : Code.Success}

def add_suboption(inputData={}) :
    fields = ["option_uid", "suboption_name", "price", "amount"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    option = ProductOption.query.get(inputData["option_uid"])

    # 옵션이 존재하지 않을 때,
    if option == None :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption}

    store = StoreInfo.query.get(option.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    keyword = checkField(inputData)

    # 데이터 형식이 맞지 않은 경우
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    suboption = ProductSuboption.query.filter_by(
        suboption_name=inputData["suboption_name"],
        price=inputData["price"],
        amount=inputData["amount"]
    )

    # 이름+가격+남은수량 서브옵션이 이미 존재할 때,
    if suboption.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistSubOption}
    
    # 서브옵션 생성
    suboption = ProductSuboption(
        option=inputData["option_uid"],
        name=inputData["suboption_name"],
        price=inputData["price"],
        amount=inputData["amount"]
    )

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product_suboption = now_lnt

    DB.session.add(suboption)
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success, "uid" : suboption.unique_product_suboption}

def modify_suboption(inputData={}) :
    fields = ["suboption_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    suboption = ProductSuboption.query.get(inputData["suboption_uid"])

    # 해당 서브옵션이 존재하지 않을 때,
    if suboption == None :
        return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}

    option = ProductOption.query.get(suboption.unique_product_option)
    store = StoreInfo.query.get(option.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 수정된 데이터 임시 적용
    option_uid = suboption.unique_product_option
    suboption_name = suboption.suboption_name
    price = suboption.price
    amount = suboption.amount

    if "option_uid" in inputData :
        option_uid = inputData["option_uid"]
    if "suboption_name" in inputData :
        suboption_name = inputData["suboption_name"]
    if "price" in inputData :
        price = inputData["price"]
    if "amount" in inputData :
        amount = inputData["amount"]
    
    # 데이터 형식 검사
    keyword = checkField(inputData)

    ## 추가로 수정하려는 옵션 존재 유무 검사
    modify_option = ProductOption.query.get(option_uid)
    if modify_option == None :
        keyword.append("option_uid")
    
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 수정된 옵션이 이미 존재하는지 검사
    modify_suboption = ProductSuboption.query.filter_by(
        unique_product_option=option_uid,
        suboption_name=suboption_name,
        price=price,
        amount=amount
    )

    if modify_suboption.count() > 0 :
        return {"result" : "Invalid", "code" : Code.AlreadyExistSubOption}
    
    # 서브옵션 수정
    suboption.unique_product_option = option_uid
    suboption.suboption_name = suboption_name
    suboption.price = price
    suboption.amount = amount

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product_suboption = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def delete_suboption(inputData={}) :
    fields = ["suboption_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    suboption = ProductSuboption.query.get(inputData["suboption_uid"])

    # 서브옵션이 존재하지 않을 때,
    if suboption == None :
        return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}
    
    option = ProductOption.query.get(suboption.unique_product_option)
    store = StoreInfo.query.get(option.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 서브옵션 삭제
    suboption.disable_date = datetime.now()

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product_suboption = now_lnt

    DB.session.commit()

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

    product = Product.query.get(inputData["product_uid"])

    # 존재하지 않는 상품일 때,
    if product == None :
        return {"result" : "Invalid", "code" : Code.NotExistProduct}
    
    store = StoreInfo.query.get(product.unique_store_info)
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 상품-옵션 관계 집합 생성
    relations = ProductOptionRelations.query.filter_by(unique_product=inputData["product_uid"])
    option_uids = [rel.unique_product_option for rel in relations.all()]

    create = list(set(inputData["option_uid"]).difference(set(option_uids))) # 집합 A - B
    delete = list(set(option_uids).difference(set(inputData["option_uid"]))) # 집합 B - A
    
    not_exist_options = []

    # 생성하려는 상품-옵션 관계 중, 존재하지 않는 옵션이 하나라도 있을 때,
    for uid in create :
        option = ProductOption.query.get(uid)

        if option == None:
            not_exist_options.append(uid)

    if len(not_exist_options) > 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProductOption, "keyword" : not_exist_options}

    # 상품-옵션 관계 수정
    # 1. 삭제
    for option_uid in delete :
        relation = relations.filter_by(unique_product_option=option_uid).first()
        DB.session.delete(relation)
    
    # 2. 생성
    for option_uid in create :
        relation = ProductOptionRelations(product=inputData["product_uid"], option=option_uid)
        DB.session.add(relation)

    # 버전 업데이트
    now_lnt = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.product_option_relations = now_lnt

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def get_group_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.query.get(inputData["store_uid"])
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    records = ProductGroup.query.filter_by(unique_store_info=inputData["store_uid"], disable_date=None).all() # 카테고리 목록

    # dict형으로 변환
    groups = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        groups.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "groups" : groups}

def get_product_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.query.get(inputData["store_uid"])
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    records = Product.query.filter_by(unique_store_info=inputData["store_uid"], disable_date=None).all() # 상품 목록

    # dict형으로 변환
    products = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)

        relations = ProductOptionRelations.query.filter_by(unique_product=dictRec["unique_product"]).all()

        dictRec["options"] = [rel.unique_product_option for rel in relations]
        products.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "products" : products}

def get_option_list(inputData={}) :
    # 필수 필드가 누락됐을 때,
    fields = ["store_uid"]
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    # 존재하지 않는 매장일 때,
    store = StoreInfo.query.get(inputData["store_uid"])
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.get(store.unique_admin)

    # 요청자와 소유자가 일치하지 않을 때,
    if user.user_id != inputData["user_id"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    records = ProductOption.query.filter_by(unique_store_info=inputData["store_uid"], disable_date=None).all() # 옵션 목록

    # dict형으로 변환
    options = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        options.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "options" : options}
