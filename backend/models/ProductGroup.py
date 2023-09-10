import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

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

def getGroups(store_id=-1) :
    # uid, name
    return

def setGroup(uid=-1, name="") :
    return

def add(userData) :
    # require : store uid, group name
    sql = f"""INSERT INTO Product_group (unique_store_info, group_name, disable_date)
    VALUES('{userData["store_uid"]}', '{userData["group_name"]}', NULL);"""

    mysql.execute(SQL=sql)

    return findGroup(store_uid=userData["store_uid"], name=userData["group_name"])

def remove(uid=-1) :
    return