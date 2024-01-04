import sys
import os
import shutil
import re
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from backend.utils import *
from statusCode import *
from flask_jwt_extended import *
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
from helpers.store import *

def checkField(data) :
    keyword = []

    if "name" in data :
        data["name"] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", data["name"]).replace("\n", "").strip()
        if len(data["name"]) < MinLength.store_name or len(data["name"]) > MaxLength.store_name :
            keyword.append("name")

    if "owner" in data :
        data["owner"] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", data["owner"]).replace("\n", "").strip()
        if len(data["owner"]) < MinLength.store_owner or len(data["owner"]) > MaxLength.store_owner :
            keyword.append("owner")

    if "address" in data :
        data["address"] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", data["address"]).replace("\n", "").strip()
        if len(data["address"]) < MinLength.store_address or len(data["address"]) > MaxLength.store_address :
            keyword.append("address")

    if "tel_num" in data :
        data["tel_num"] = re.sub(r"[^0-9-]", "", data["tel_num"])
        if len(data["tel_num"]) < MinLength.store_tel_number or len(data["tel_num"]) > MaxLength.store_tel_number :
            keyword.append("tel_num")

    if "count" in data :
        if data["count"] < 0 :
            keyword.append("count")

    return keyword

def addStore(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    fields = ["user_id", "name", "owner", "address", "tel_num", "count"]
    for field in fields :
        if field not in inputStoreInfo :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    keyword = checkField(inputStoreInfo)

    # 데이터 형식이 잘못 됐을 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    user = Admins.query.filter_by(user_id=inputStoreInfo["user_id"]).first()

    # 아이디로 유저가 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    store = StoreInfo.query.filter_by(store_name=inputStoreInfo["name"]).first()

    # 해당 매장이름을 가진 매장이 존재할 때,
    if store != None :
        return {"result" : "Invalid", "code" : Code.AlreadyExistStore}

    # DB에 매장 추가
    store = StoreInfo(
        admin=user.unique_admin,
        name=inputStoreInfo["name"],
        owner=inputStoreInfo["owner"],
        address=inputStoreInfo["address"],
        number=inputStoreInfo["tel_num"],
        count=inputStoreInfo["count"]
    )
    DB.session.add(store)
    DB.session.commit()

    # 추가한 매장 가져오기
    store = StoreInfo.query.filter_by(
        unique_admin=user.unique_admin,
        store_name=inputStoreInfo["name"],
        store_owner=inputStoreInfo["owner"],
        store_address=inputStoreInfo["address"],
        store_tel_number=inputStoreInfo["tel_num"],
        table_count=inputStoreInfo["count"]
    ).first()

    # 테이블을 1부터 순차적으로 추가
    for table_n in range(1, inputStoreInfo["count"]+1) :
        table = TableList(store=store.unique_store_info, number=table_n, state=0)
        DB.session.add(table)
    
    # 버전 추가
    ver = Version(store=store.unique_store_info)

    DB.session.add(ver)
    DB.session.commit()
    
    # 폴더 추가
    store_image_path = Path.ADMIN + "/" + str(user.unique_admin) + "/store/" + str(store.unique_store_info) + "/product"
    if os.path.exists(store_image_path) :
        shutil.rmtree(store_image_path)
    os.makedirs(store_image_path)

    return {"result" : "Success", "code" : Code.Success, "uid" : store.unique_store_info}

def change_store_info(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    keyword = checkField(inputStoreInfo)
    
    # 데이터 형식이 잘못 된 경우,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    store = StoreInfo.query.get(inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.filter_by(user_id=inputStoreInfo["user_id"]).first()

    # 해당 유저가 존재하지 않을 경우,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = dict(user.__dict__)
    
    # 요청한 사람의 매장이 아닌 경우,
    if user["unique_admin"] != store.unique_admin :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 매장 정보 수정
    modify_store(store=store, inputStoreInfo=inputStoreInfo)
    
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}
    
def delete_store(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.query.get(inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    user = Admins.query.filter_by(user_id=inputStoreInfo["user_id"]).first()

    # 해당 유저가 존재하지 않을 경우,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 요청한 사람의 매장이 아닌 경우,
    if user.unique_admin != store.unique_admin :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    now = datetime.now()

    # 매장 삭제
    store.disable_date = now

    # 테이블 삭제
    modify_store(store=store, inputStoreInfo={"count" : 0})
        
    # 상품 그룹 삭제
    groups = ProductGroup.query.filter_by(unique_store_info=store.unique_store_info).all()
    for group in groups :
        group.disable_date = now

    # 상품 삭제
    products = Product.query.filter_by(unique_store_info=store.unique_store_info).all()
    for product in products :
        product.disable_date = now
        
        # 상품-옵션 관계 삭제
        relations = ProductOptionRelations.query.filter_by().all()
        for relation in relations :
            DB.session.delete(relation)

    # 상품 옵션 삭제
    options = ProductOption.query.filter_by(unique_store_info=store.unique_store_info).all()
    for option in options :
        option.disable_date = now

        # 상품 서브옵션 삭제
        suboptions = ProductSuboption.query.filter_by(unique_product_option=option.unique_product_option).all()
        for suboption in suboptions :
            suboption.disable_date = now

    # 주문 삭제
    orders = OrderList.query.filter_by(unique_store_info=store.unique_store_info).all()
    for order in orders :
        order.order_state = OrderState.SellerCancel
        order.last_modify_date = now

        # 선택된 옵션 삭제
        selected_options = SelectedOption.query.filter_by(unique_order=order.unique_order).all()
        for selected_option in selected_options :
            selected_option.disable_date = now
    
    # 버전 삭제
    now_lnt = int(now.strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간
    version = Version.query.get(store.unique_store_info)
    version.table_list = now_lnt
    version.product_group = now_lnt
    version.product = now_lnt
    version.product_option = now_lnt
    version.product_option_relations = now_lnt
    version.product_suboption = now_lnt
    version.order_list = now_lnt
    version.disable_date = now
    
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def get_my_stores(user_id='') :
    user = Admins.query.filter_by(user_id=user_id).first()

    # 해당 유저가 존재하지 않을 경우,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 보유 매장 불러오기
    records = StoreInfo.query.filter_by(unique_admin=user.unique_admin, disable_date=None).all() # 삭제되지 않은 보유 매장 컬럼 리스트
    
    # dict형으로 변환
    stores = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        stores.append(dictRec)
    
    return {"result" : "Success", "code" : Code.Success, "stores" : stores}

def get_store_info(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    user = Admins.query.filter_by(user_id=inputStoreInfo["user_id"]).first()

    # 해당 유저가 존재하지 않을 경우,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    store = StoreInfo.query.get(inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    # 삭제된 매장일 경우,
    if store.disable_date != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 요청한 사람의 매장이 아닌 경우,
    if user.unique_admin != store.unique_admin :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    store = dict(store.__dict__)
    store.pop('_sa_instance_state', None)
    
    return {"result" : "Success", "code" : Code.Success, "store" : store}
