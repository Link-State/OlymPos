import sys
import os
import datetime

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

def product_order(inputData={}) :
    fields = ["SSAID", "store_uid", "product_uid", "table", "amount"]
    
    # 필수 필드가 누락 됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    store = StoreInfo.getStore(uid=inputData["store_uid"])

    # 존재하지 않는 매장일 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    product = Product.getProduct(uid=inputData["product_uid"])

    # 존재하지 않는 상품일 때,
    if len(product) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistProduct}

    table = TableList.getTable(store_uid=inputData["store_uid"], tableNum=inputData["table"])

    # 존재하지 않는 테이블 번호일 때,
    if len(table) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistTable}

    # 주문을 시도한 기기의 SSAID, 주문을 시도한 테이블의 isLogin DB값과 같은지 체크
    if table["isLogin"] != inputData["SSAID"] :
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
            
            option = ProductOption.getOption(uid=elem["option"])
            suboption = ProductSuboption.getSubOption(uid=elem["suboption"])

            # 3. 선택한 옵션의 List의 원소(=옵션 및 서브옵션)가 존재하지 않는 옵션, 서브옵션일 때,
            if len(option) <= 0 :
                return {"result" : "Invalid", "code" : Code.NotExistProductOption}
            if len(suboption) <= 0 :
                return {"result" : "Invalid", "code" : Code.NotExistProductSuboption}
            
    inputData["order_date"] = datetime.datetime.now()

    # 주문서 생성
    OrderList.add(inputData)

    order_uid = OrderList.findOrder(store_uid=inputData["store_uid"], date=inputData["order_date"])

    return {"result" : "Success", "code" : Code.Success, "uid" : order_uid}