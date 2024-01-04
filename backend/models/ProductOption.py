import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from backend.utils import *
from models import mysql
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ProductOption(DB.Model) :
    __tablename__ = "Product_option"

    unique_product_option = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    option_name = Column(String(MaxLength.option_name), nullable=False)
    price = Column(Integer, nullable=False)
    suboption_offer = Column(Integer, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, name, price, offer, disable=None) :
        self.unique_store_info = store
        self.option_name = name
        self.price = price
        self.suboption_offer = offer
        self.disable_date = disable


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
def getOptions(store_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''
    
    sql = f"""
    SELECT unique_product_option, unique_store_info, option_name, price, suboption_offer{select}
    FROM Product_option
    WHERE unique_store_info = {store_uid}{where};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 각 매장에 대한 날짜 포맷팅
    for st in result :
        if "disable_date" not in st :
            break
        if st["disable_date"] != None :
            date = st["disable_date"].isoformat(sep=' ', timespec="seconds")
            st["disable_date"] = '-'.join(date.split(':'))

    return result

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

    return result[0]

def setStore(uid=-1, id=-1) :
    return

def setProduct(uid=-1, product_id=-1) :
    return

def setName(uid=-1, name="") :
    sql = f"""
    UPDATE Product_option
    SET option_name = '{name}'
    WHERE unique_product_option = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def setPrice(uid=-1, price=0) :
    sql = f"""
    UPDATE Product_option
    SET price = {price}
    WHERE unique_product_option = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def setIsOffer(uid=-1, isoffer=0) :
    sql = f"""
    UPDATE Product_option
    SET suboption_offer = {isoffer}
    WHERE unique_product_option = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def add(userData) :
    # require : product id, name, price, isOffer
    # 생성 후 UID 자동 반환

    sql = f"""INSERT INTO Product_option (unique_store_info, option_name, price, suboption_offer, disable_date)
    VALUES('{userData["store_uid"]}', '{userData["option_name"]}', '{userData["price"]}', '{userData["isoffer"]}', NULL);"""

    mysql.execute(SQL=sql)

    return findOption(store_uid=userData["store_uid"], name=userData["option_name"], price=userData["price"], isoffer=userData["isoffer"])

def remove(uid=-1, date=datetime.datetime.now()) :
    sql = f"""
    UPDATE Product_option
    SET disable_date = {date}
    WHERE unique_product_option = {uid};
    """
    
    mysql.execute(SQL=sql)

    return