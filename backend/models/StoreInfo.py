import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql


def getStores(admin_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''
    
    sql = f"""
    SELECT unique_store_info, unique_admin, store_name, store_owner, store_address, store_tel_number, table_count{select}
    FROM Store_info
    WHERE unique_admin = {admin_uid}{where};
    """

    return mysql.execute(SQL=sql, fetch=True)

def getStore(uid=-1) :
    sql = f"""
    SELECT unique_store_info, unique_admin, store_name, store_owner, store_address, store_tel_number, table_count, disable_date
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
    # Table List에 1부터 num까지 순차적으로 생성
    return

def setIsLogin(uid=-1, islogin=0) :
    sql = f"""
    UPDATE Store_info
    SET isLogin = {islogin}
    WHERE unique_store_info = {uid};
    """

    mysql.execute(SQL=sql)
    
    return

def add(**kwargs) :
    # admin uid, name, owner, address, tel num
    return

def remove(uid=-1) :
    return