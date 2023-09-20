import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql
from models import TableList

def findStore(uid=-1, name="") :
    sql = f"""
    SELECT unique_store_info
    FROM Store_info
    WHERE unique_admin = {uid} and store_name = '{name}';
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 해당 아이디와 이름의 매장이 없음
    if len(result) != 1 :
        return -1

    return result[0]["unique_store_info"]

def getStores(admin_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''
    
    sql = f"""
    SELECT unique_store_info, unique_admin, store_name, store_owner, store_address, store_tel_number, table_count, last_modify_date{select}
    FROM Store_info
    WHERE unique_admin = {admin_uid}{where};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    # 각 매장에 대한 날짜 포맷팅
    for st in result :
        date = st["last_modify_date"].isoformat(sep=' ', timespec="seconds")
        st["last_modify_date"] = '-'.join(date.split(':'))
        if st["disable_date"] != None :
            date = st["disable_date"].isoformat(sep=' ', timespec="seconds")
            st["disable_date"] = '-'.join(date.split(':'))

    return result

def getStore(uid=-1) :
    sql = f"""
    SELECT unique_store_info, unique_admin, store_name, store_owner, store_address, store_tel_number, table_count, last_modify_date, disable_date
    FROM Store_info
    WHERE unique_store_info = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 매장 정보 없음
    if len(result) != 1 :
        return dict()
    
    # 날짜 포맷
    date = result[0]["last_modify_date"].isoformat(sep=' ', timespec="seconds")
    result[0]["last_modify_date"] = '-'.join(date.split(':'))

    if result[0]["disable_date"] != None :
        date = result[0]["disable_date"].isoformat(sep=' ', timespec="seconds")
        result[0]["disable_date"] = '-'.join(date.split(':'))

    return result[0]

def setAdminUID(uid=-1, admin_uid=-1) :
    return

def setName(uid=-1, name="") :
    sql = f"""
    UPDATE Store_info
    SET store_name = '{name}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setOwner(uid=-1, owner="") :
    sql = f"""
    UPDATE Store_info
    SET store_owner = '{owner}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setAddress(uid=-1, address="") :
    sql = f"""
    UPDATE Store_info
    SET store_address = '{address}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setTelNum(uid=-1, tel="") :
    sql = f"""
    UPDATE Store_info
    SET store_tel_number = '{tel}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setTableCount(uid=-1, num=-1) :
    sql = f"""
    UPDATE Store_info
    SET table_count = '{num}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setIsLogin(uid=-1, islogin=0) :
    sql = f"""
    UPDATE Store_info
    SET isLogin = {islogin}
    WHERE unique_store_info = {uid};
    """

    mysql.execute(SQL=sql)
    
    return

def setLastModifyDate(uid=-1, date=datetime.datetime.now()) :
    sql = f"""
    UPDATE Store_info
    SET last_modify_date = '{date}'
    WHERE unique_store_info = {uid};
    """

    mysql.execute(SQL=sql)
    
    return

def add(userData) :
    now = datetime.datetime.now()
    sql = f"""INSERT INTO Store_info (unique_admin, store_name, store_owner, store_address, store_tel_number, table_count, last_modify_date, disable_date)
    VALUES('{userData["unique_admin"]}', '{userData["name"]}', '{userData["owner"]}', '{userData["address"]}', '{userData["tel_num"]}', '{userData["count"]}', '{now}', NULL);"""

    mysql.execute(SQL=sql)

    return

def remove(uid=-1) :
    now = datetime.datetime.now()

    sql = f"""
    UPDATE Store_info
    SET disable_date = '{now}'
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return