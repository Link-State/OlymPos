import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
from models.mysql import DB
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey

class Product(DB.Model) :
    __tablename__ = "Product"

    unique_product = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey(''), nullable=False)
    unique_product_group = Column(Integer, ForeignKey(''), nullable=False)
    product_name = Column(String(MaxLength.product_name), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(Text, nullable=True, default="")
    description = Column(Text, nullable=True, default="")
    amount = Column(Integer, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, group, name, price, amount, disable=None, img="", descrp="") :
        self.unique_store_info = store
        self.unique_product_group = group
        self.product_name = name
        self.price = price
        self.image = img
        self.description = descrp
        self.amount = amount
        self.disable_date = disable


def getProducts(store_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''
    
    sql = f"""
    SELECT unique_product, unique_store_info, unique_product_group, product_name, price, image, description, amount{select}
    FROM Product
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

def getProduct(uid=-1) :
    sql = f"""
    SELECT unique_product, unique_store_info, unique_product_group, product_name, price, image, description, amount, disable_date
    FROM Product
    WHERE unique_product = {uid};
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

def setGroupID(uid=-1, id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setImage(uid=-1, image="") :
    return

def setDescription(uid=-1, descript="") :
    return

def setAmount(uid=-1, amount=-1) :
    return

def add(**kwargs) :
    # require : group uid, name, price
    return

def remove(uid=-1) :
    return