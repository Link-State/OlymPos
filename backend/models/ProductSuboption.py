import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

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
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setAmount(uid=-1, amount=-1) :
    return

def add(**kwargs) :
    # require : product id, name, price, amount
    return

def remove(uid=-1) :
    return