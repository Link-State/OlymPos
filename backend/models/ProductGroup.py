import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ProductGroup(DB.Model) :
    __tablename__ = "Product_group"

    unique_product_group = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    group_name = Column(String(MaxLength.group_name), nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, name, disable=None) :
        self.unique_store_info = store
        self.group_name = name
        self.disable_date = disable


# 해당 매장의 카테고리 목록 반환
def findGroup(store_uid=-1, name='') :
    sql = f"""
    SELECT unique_product_group
    FROM Product_group
    WHERE unique_store_info = {store_uid} and group_name = '{name}';
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return -1

    return result[0]["unique_product_group"]

def getGroups(store_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''

    sql = f"""
    SELECT unique_product_group, unique_store_info, group_name{select}
    FROM Product_group
    WHERE unique_store_info = {store_uid}{where};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if include_disable :
        for group in result :
            if group["disable_date"] != None :
                date = group["disable_date"].isoformat(sep=' ', timespec="seconds")
                group["disable_date"] = "-".join(date.split(":"))

    return result

def getGroup(uid=-1) :
    # unique_product_group, unique_store_info, group_name, disable_date
    sql = f"""
    SELECT unique_product_group, unique_store_info, group_name, disable_date
    FROM Product_group
    WHERE unique_product_group = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return dict()
    
    # 날짜 포맷
    if result[0]["disable_date"] != None :
        date = result[0]["disable_date"].isoformat(sep=' ', timespec="seconds")
        result[0]["disable_date"] = '-'.join(date.split(':'))

    return result[0]

def setName(uid=-1, name="") :
    sql = f"""
    UPDATE Product_group
    SET group_name = '{name}'
    WHERE unique_product_group = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def add(userData) :
    # require : store uid, group name
    sql = f"""INSERT INTO Product_group (unique_store_info, group_name, disable_date)
    VALUES('{userData["store_uid"]}', '{userData["group_name"]}', NULL);"""

    mysql.execute(SQL=sql)

    return findGroup(store_uid=userData["store_uid"], name=userData["group_name"])

def remove(uid=-1, date=datetime.datetime.now()) :
    sql = f"""
    UPDATE Product_group
    SET disable_date = '{date}'
    WHERE unique_product_group = {uid};
    """
    
    mysql.execute(SQL=sql)

    return