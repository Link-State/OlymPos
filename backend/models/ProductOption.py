import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

def findOption(store_uid=-1, name='', price=0, isoffer=0) :
    sql = f"""
    SELECT unique_product_option
    FROM Product_option
    WHERE unique_store_info = {store_uid} and option_name = '{name}' and price = {price} and suboption_offer = {isoffer};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return -1

    return result[0]["unique_product_option"]

# 해당 제품의 옵션 목록 반환
def getOptions(product_uid=-1) :
    return

def getOption(uid=-1) :
    sql = f"""
    SELECT unique_product_option, unique_store_info, option_name, price, suboption_offer, disable_date
    FROM Product_option
    WHERE unique_product_option = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    # 매장 정보 없음
    if len(result) != 1 :
        return dict()
    
    # 날짜 포맷
    if result[0]["disable_date"] != None :
        date = result[0]["disable_date"].isoformat(sep=' ', timespec="seconds")
        result[0]["disable_date"] = '-'.join(date.split(':'))

    return result

def setStore(uid=-1, id=-1) :
    return

def setProduct(uid=-1, product_id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setIsOffer(uid=-1, isoffer=0) :
    return

def add(userData) :
    # require : product id, name, price, isOffer
    # 생성 후 UID 자동 반환

    sql = f"""INSERT INTO Product_option (unique_store_info, option_name, price, suboption_offer, disable_date)
    VALUES('{userData["store_uid"]}', '{userData["option_name"]}', '{userData["price"]}', '{userData["isoffer"]}', NULL);"""

    mysql.execute(SQL=sql)

    return findOption(store_uid=userData["store_uid"], name=userData["option_name"], price=userData["price"], isoffer=userData["isoffer"])

def remove(uid=-1) :
    return