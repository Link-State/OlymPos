import sys
import os
import shutil
import re
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
from models.Version import Version

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
        if data["count"] < 1 :
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

    # 폴더 추가
    store_image_path = Path.STORE + "/" + str(store.unique_store_info)
    if os.path.exists(store_image_path) :
        shutil.rmtree(store_image_path)
    os.mkdir(store_image_path)

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
    if "name" in inputStoreInfo :
        store.store_name = inputStoreInfo["name"]

    if "owner" in inputStoreInfo :
        store.store_owner = inputStoreInfo["owner"]

    if "address" in inputStoreInfo :
        store.store_address = inputStoreInfo["address"]

    if "tel_num" in inputStoreInfo :
        store.store_tel_number = inputStoreInfo["tel_num"]
    
    if "count" in inputStoreInfo :
        tables = TableList.query.filter_by(unique_store_info=store.unique_store_info).order_by(TableList.table_number).all()

        current = store.table_count # 현재 활성화된 테이블 갯수
        maximum = len(tables) # DB에 생성된 테이블 갯수
        request = inputStoreInfo["count"] # 활성화할 테이블 갯수
        now = datetime.now()
        now_lnt = int(now.strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간

        # 현재 활성화된 테이블 갯수와 활성화할 테이블 갯수가 같지 않을 때, DB상 기록된 테이블 갯수 수정
        if request != current :
            store.table_count = request
            store.last_modify_date = now

            version = Version.query.get(store.unique_store_info)
            version.table_list = now_lnt
        
        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 클 경우,
        if request > current :
            for i in range(current + 1, maximum + 1) :
                # 재활성화
                tables[i-1].disable_date = None
            for i in range(maximum + 1, request + 1) :
                # 생성
                table = TableList(store=store.unique_store_info, number=i, state=0)
                DB.session.add(table)

        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 작을 경우,
        elif request < current :
            # 비활성화
            for i in range(request + 1, current + 1) :
                tables[i-1].isLogin = ""
                tables[i-1].table_state = 0
                tables[i-1].disable_date = now
    
    DB.session.commit()

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