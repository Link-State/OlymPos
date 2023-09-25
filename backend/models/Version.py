import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def getVersion(store_uid=-1) :
    sql = f"""
    SELECT unique_store_info, table_list, product_group, product, product_option, product_suboption
    FROM Version
    WHERE unique_store_info = {store_uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 버전 정보 없음
    if len(result) != 1 :
        return dict()

    return result[0]

def set() :
    return