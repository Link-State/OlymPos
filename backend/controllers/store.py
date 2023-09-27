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

    if "name" in data :
        if len(data["name"]) < MinLength.store_name or len(data["name"]) > MaxLength.store_name :
            keyword.append("name")

    if "owner" in data :
        if len(data["owner"]) < MinLength.store_owner or len(data["owner"]) > MaxLength.store_owner :
            keyword.append("owner")

    if "address" in data :
        if len(data["address"]) < MinLength.store_address or len(data["address"]) > MaxLength.store_address :
            keyword.append("address")

    if "tel_num" in data :
        if len(data["tel_num"]) < MinLength.store_tel_number or len(data["tel_num"]) > MaxLength.store_tel_number :
            keyword.append("tel_num")

    if "count" in data :
        if data["count"] < 1 :
            keyword.append("count")

    return keyword

def addStore(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    fields = ["user_id", "name", "owner", "address", "tel_num", "count"]
    for field in fields :
        if field not in inputStoreInfo :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    uid = Admins.findUID(id=inputStoreInfo["user_id"])

    # 유저 아이디로 고유번호가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    store_uid = StoreInfo.findStore(uid=uid, name=inputStoreInfo["name"])

    # 이미 해당 유저에게 존재하는 매장일 때,
    if store_uid != -1 :
        store = StoreInfo.getStore(uid=store_uid)
        
        # 삭제된 매장일 때,
        if store["disable_date"] != None :
            return {"result" : "Invalid", "code" : Code.DeletedData}
        
        return {"result" : "Invalid", "code" : Code.AlreadyExistStore}
    
    keyword = checkField(inputStoreInfo)

    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    inputStoreInfo["unique_admin"] = uid

    # DB에 매장 추가
    StoreInfo.add(inputStoreInfo)

    store_uid = StoreInfo.findStore(uid=uid, name=inputStoreInfo["name"])

    # 테이블을 1부터 순차적으로 추가
    for table in range(1, inputStoreInfo["count"]+1) :
        TableList.add({"store_uid" : store_uid, "table":table})
    
    # 버전 추가
    Version.add(uid=store_uid)

    return {"result" : "Success", "code" : Code.Success, "uid" : store_uid}

def change_store_info(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    uid = Admins.findUID(id=inputStoreInfo["user_id"])

    # 해당 유저가 존재하지 않을 경우,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 요청한 사람의 매장이 아닌 경우,
    if uid != store["unique_admin"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}

    keyword = checkField(inputStoreInfo)
    
    # 데이터 형식이 잘못 된 경우,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 매장 정보 수정
    store_uid = inputStoreInfo["store_uid"]
    if "name" in inputStoreInfo :
        StoreInfo.setName(uid=store_uid, name=inputStoreInfo["name"])

    if "owner" in inputStoreInfo :
        StoreInfo.setOwner(uid=store_uid, owner=inputStoreInfo["owner"])

    if "address" in inputStoreInfo :
        StoreInfo.setAddress(uid=store_uid, address=inputStoreInfo["address"])

    if "tel_num" in inputStoreInfo :
        StoreInfo.setTelNum(uid=store_uid, tel=inputStoreInfo["tel_num"])
    
    if "count" in inputStoreInfo :
        tables = TableList.getTables(store_uid=store_uid)

        current = store["table_count"] # 현재 활성화된 테이블 갯수
        maximum = len(tables) # DB에 생성된 테이블 갯수
        request = inputStoreInfo["count"] # 활성화할 테이블 갯수

        # 현재 활성화된 테이블 갯수와 활성화할 테이블 갯수가 같지 않을 때, DB상 기록된 테이블 갯수 수정
        if request != current :
            StoreInfo.setTableCount(uid=store_uid, num=request)
            Version.setTableList(uid=store_uid)
        
        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 클 경우,
        if request > current :
            for i in range(current + 1, maximum + 1) :
                # 재활성화
                TableList.restore(store_uid=store_uid, tableNum=i)
            for i in range(maximum + 1, request + 1) :
                # 생성
                TableList.add({"store_uid" : store_uid, "table" : i})
        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 작을 경우,
        elif request < current :
            # 비활성화
            for i in range(request + 1, current + 1) :
                TableList.setIsLogin(store_uid=store_uid, tableNum=i, islogin='')
                TableList.remove(store_uid=store_uid, tableNum=i)
    
    StoreInfo.setLastModifyDate(uid=store_uid)

    return {"result" : "Success", "code" : Code.Success}
    
def delete_store(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    uid = Admins.findUID(id=inputStoreInfo["user_id"])

    # 해당 유저가 존재하지 않을 경우,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 요청한 사람의 매장이 아닌 경우,
    if uid != store["unique_admin"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 매장 삭제
    StoreInfo.remove(uid=inputStoreInfo["store_uid"])

    # 테이블 삭제
    for i in range(1, store["table_count"]+1) :
        TableList.remove(store_uid=inputStoreInfo["store_uid"], tableNum=i)

    # 상품 그룹 삭제
    ## 매장 고유번호로 그룹 찾을 것.

    # 상품 삭제
    ## 매장 고유번호로 상품 찾을 것.

    # 상품 옵션 삭제
    ## 매장 고유번호로 옵션 찾을 것.

    # 상품-옵션 관계 삭제
    ## 상품 고유번호로 관계 삭제할 것.

    # 상품 서브옵션 삭제
    ## 옵션 고유번호로 서브옵션 찾을 것.

    # 주문 삭제
    ## 매장 고유번호로 주문서 찾을 것.

    # 선택된 옵션 삭제
    ## 주문서 고유번호로 선택된옵션 찾을 것.

    return {"result" : "Success", "code" : Code.Success}

def get_my_stores(user_id='') :
    uid = Admins.findUID(id=user_id)

    # 해당 유저가 존재하지 않을 경우,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 보유 매장 불러오기
    stores = StoreInfo.getStores(admin_uid=uid)
    
    return {"result" : "Success", "code" : Code.Success, "stores" : stores}

def get_store_info(inputStoreInfo={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in inputStoreInfo :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=inputStoreInfo["store_uid"])

    # 매장이 존재하지 않는 경우,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    uid = Admins.findUID(id=inputStoreInfo["user_id"])

    # 해당 유저가 존재하지 않을 경우,
    if uid == -1 :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 요청한 사람의 매장이 아닌 경우,
    if uid != store["unique_admin"] :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    return {"result" : "Success", "code" : Code.Success, "store" : store}