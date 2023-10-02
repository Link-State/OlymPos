import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

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

def add(**kwargs) :
    # require : product id, name, price, isOffer
    return

def remove(uid=-1) :
    return