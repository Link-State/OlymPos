import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
from models.mysql import DB
from sqlalchemy import Column, Integer, DateTime, ForeignKey

class OrderList(DB.Model) :
    __tablename__ = "Order_list"

    unique_order = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    unique_product = Column(Integer, ForeignKey('Product.unique_product'), nullable=False)
    table_number = Column(Integer, ForeignKey('Table_list.table_number'), nullable=True)
    amount = Column(Integer, nullable=False)
    order_state = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)

    def __init__(self, store, product, amount, state, date, number=None) :
        self.unique_store_info = store
        self.unique_product = product
        self.table_number = number
        self.amount = amount
        self.order_state = state
        self.order_date = date

def findOrder(store_uid=-1, date=datetime.datetime.now()) :

    sql = f"""
    SELECT unique_order
    FROM Order_list
    WHERE unique_store_info = {store_uid} and DATE_FORMAT(order_date, '%Y-%m-%d %H:%i:%s') = '{date.isoformat(sep=' ', timespec="seconds")}';
    """

    result = mysql.execute(SQL=sql, fetch=True)

    uids = []
    for uid in result :
        uids.append(uid["unique_order"])

    return uids

def getOrders(store_uid=-1) :

    sql = f"""
    SELECT unique_order, unique_store_info, unique_product, table_number, amount, order_state, order_date
    FROM Order_list
    WHERE unique_store_info = {store_uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    # 각 주문에 대한 날짜 포맷팅
    for st in result :
        if st["order_date"] != None :
            date = st["order_date"].isoformat(sep=' ', timespec="seconds")
            st["order_date"] = '-'.join(date.split(':'))
    
    return result

def getOrder(uid=-1) :

    sql = f"""
    SELECT unique_order, unique_store_info, unique_product, table_number, amount, order_state, order_date
    FROM Order_list
    WHERE unique_order = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return dict()
    
    # 날짜 포맷
    date = result[0]["order_date"].isoformat(sep=' ', timespec="seconds")
    result[0]["order_date"] = '-'.join(date.split(':'))

    return result

def setProduct(uid=-1, product_id=-1) :
    return

def setTableNum(uid=-1, num=-1) :
    return

def setAmount(uid=-1, amount=-1) :
    return

def setState(uid=-1, state=0) :
    
    sql = f"""
    UPDATE Order_list
    SET order_state = '{state}'
    WHERE unique_order = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setDate(uid=-1, date=datetime.datetime.now()) :
    return

def add(userData) :
    sql = f"""INSERT INTO Order_list (unique_store_info, unique_product, table_number, amount, order_state, order_date)
    VALUES('{userData["store_uid"]}', '{userData["product_uid"]}', '{userData["table"]}', '{userData["amount"]}', '{0}', '{userData["order_date"]}');"""

    mysql.execute(SQL=sql)

    return

def remove(uid=-1) :
    return
