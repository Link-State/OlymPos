import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
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

def product_order(inputData={}) :
    fields = ["SSAID", "store_uid", "product_uid", "table", "amount"]
    
    # 필수 필드가 누락 됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    store = StoreInfo.query.get(inputData["store_uid"])

    # 존재하지 않는 매장일 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    product = Product.query.get(inputData["product_uid"])

    # 존재하지 않는 상품일 때,
    if product == None :
        return {"result" : "Invalid", "code" : Code.NotExistProduct}

    table = TableList.query.get({"unique_store_info" : inputData["store_uid"], "table_number" : inputData["table"]})

    # 존재하지 않는 테이블 번호일 때,
    if table == None :
        return {"result" : "Invalid", "code" : Code.NotExistTable}

    # 주문을 시도한 기기의 SSAID, 주문을 시도한 테이블의 isLogin DB값과 같은지 체크
    if table.isLogin == "" or table.isLogin != inputData["SSAID"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 선택한 옵션이 있을 경우,
    if "options" in inputData and len(inputData["options"]) > 0 :
        options = inputData["options"]

        # 1. 선택한 옵션이 List 형식이 아닐 때,
        if type(options) is not type(list()) :
            return {"result" : "Invalid", "code" : Code.WrongDataForm}
        
        for elem in options :

            # 2. 선택한 옵션의 List의 원소(=옵션 및 서브옵션)가 Dict가 아닐 때
            if type(elem) is not type(dict()) :
                return {"result" : "Invalid", "code" : Code.WrongDataForm}
            
            # 3. List의 원소에 옵션 필드가 누락됐을 때,
            if "option" not in elem :
                return {"result" : "Invalid", "code" : Code.MissingRequireField}

            option = ProductOption.query.get(elem["option"])
            
            # 해당 옵션이 존재하지 않을 때,
            if option == None :
                return {"result" : "Invalid", "code" : Code.NotExistProductOption}
            
            # 4. 해당 서브옵션이 존재하지 않을 때,
            if "suboption" in elem :
                suboption = ProductSuboption.query.get(elem["suboption"])
                if suboption == None :
                    return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}

    # 주문서 생성
    order = OrderList(
        store=store.unique_store_info,
        product=product.unique_product,
        number=table.table_number,
        amount=inputData["amount"],
        state=OrderState.Receipt,
        date=datetime.now()
    )

    DB.session.add(order)
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success, "uid" : order.unique_order}

def change_order_state(inputData={}) :
    fields = ["order_uid", "state"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    order = OrderList.query.get(inputData["order_uid"])

    # 해당 주문이 존재하지 않을 때,
    if order == None :
        return {"result" : "Invalid", "code" : Code.NotExistOrder}
    
    # 주문 상태 번호가 존재하지 않을 때,
    if not OrderState.isExist(inputData["state"]) :
        return {"result" : "Invalid", "code" : Code.NotExistState}
    
    # 주문 상태 수정
    order.order_state = inputData["state"]
    
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def change_table_state(inputData={}) :
    fields = ["store_uid", "table", "state"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.query.get(inputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    table = TableList.query.get({"unique_store_info" : inputData["store_uid"], "table_number" : inputData["table"]})

    # 해당 테이블 번호가 존재하지 않을때,
    if table == None :
        return {"result" : "Invalid", "code" : Code.NotExistTable}
    
    # 해당 상태가 존재하지 않을 때,
    if not TableState.isExist(inputData["state"]) :
        return {"result" : "Invalid", "code" : Code.NotExistState}
    
    # 테이블 상태 변경
    table.table_state = inputData["state"]

    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def get_order_list(inputData={}) :
    fields = ["store_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.query.get(inputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}

    # 주문 목록 불러옴
    records = OrderList.query.filter_by(unique_store_info=inputData["store_uid"]).all() # 주문 목록

    # dict형으로 변환
    orders = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        orders.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "orders" : orders}

def get_table_list(inputData={}) :
    fields = ["store_uid"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.query.get(inputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}

    # 테이블 목록 불러옴
    records = TableList.query.filter_by(unique_store_info=inputData["store_uid"], disable_date=None).all()

    # dict형으로 변환
    tables = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        tables.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "tables" : tables}