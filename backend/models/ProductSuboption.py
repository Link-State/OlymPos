import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

def findSubOption(name="", price=0, amount=-1) :
    sql = f"""
    SELECT unique_product_suboption
    FROM Product_suboption
    WHERE suboption_name = '{name}' and price = {price} and amount = {amount};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return -1
    
    return result[0]["unique_product_suboption"]

# 해당 옵션의 서브옵션 목록 반환
def getSubOptions(option_id=-1) :
    return

def getSubOption(uid=-1) :
    sql = f"""
    SELECT unique_product_suboption, unique_product_option, suboption_name, price, amount, disable_date
    FROM Product_suboption
    WHERE unique_product_suboption = {uid};
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

def setOption(uid=-1, option_id=-1) :
    sql = f"""
    UPDATE Product_suboption
    SET unique_product_option = {option_id}
    WHERE unique_product_suboption = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def setName(uid=-1, name="") :
    sql = f"""
    UPDATE Product_suboption
    SET suboption_name = '{name}'
    WHERE unique_product_suboption = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def setPrice(uid=-1, price=0) :
    sql = f"""
    UPDATE Product_suboption
    SET price = {price}
    WHERE unique_product_suboption = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def setAmount(uid=-1, amount=-1) :
    sql = f"""
    UPDATE Product_suboption
    SET amount = {amount}
    WHERE unique_product_suboption = {uid};
    """
    
    mysql.execute(SQL=sql)

    return

def add(userData) :
    # require : product id, name, price, amount
    sql = f"""INSERT INTO Product_suboption (unique_product_option, suboption_name, price, amount, disable_date)
    VALUES('{userData["option_uid"]}', '{userData["suboption_name"]}', '{userData["price"]}', '{userData["amount"]}', NULL);"""

    mysql.execute(SQL=sql)

    return findSubOption(name=userData["suboption_name"], price=userData["price"], amount=userData["amount"])

def remove(uid=-1) :
    return