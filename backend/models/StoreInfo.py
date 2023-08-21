import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

# 해당 관리자의 매장 목록 반환
def getStores(admin_id=-1) :
    return

def getStore(uid=-1) :
    # uid, admin uid, name, owner, address, tel num
    sql = f"""
    SELECT unique_store_info, unique_admin, store_name, store_owner, store_address, store_tel_number, table_count
    FROM Store_info
    WHERE unique_store_info = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    if len(result) != 1 :
        return dict()

    return result[0]

def setAdminUID(uid=-1, admin_uid=-1) :
    return

def setName(uid=-1, name="") :
    return

def setOwner(uid=-1, owner="") :
    return

def setAddress(uid=-1, address="") :
    return

def setTelNum(uid=-1, tel="") :
    return

def setTableCount(uid=-1, num=-1) :
    return

def add(**kwargs) :
    # admin uid, name, owner, address, tel num
    # Table List에 1부터 num까지 순차적으로 생성
    return

def remove(uid=-1) :
    return