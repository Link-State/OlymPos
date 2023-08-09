import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def getTables(store_uid=-1) :
    # store uid, table num, state, isLogin
    return

def getTable(store_uid=-1, tableNum=-1) :
    sql = f"""
    SELECT unique_store_info, table_number, table_state, isLogin
    FROM Table_list
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    if len(result) != 1 :
        return dict()

    return result[0]

def setTableNum(store_uid=-1, tableNum=-1) :
    return

def setState(store_uid=-1, tableNum=-1, state=-1) :
    return

def setIsLogin(store_uid=-1, tableNum=-1, islogin=0) :
    sql = f"""
    UPDATE Table_list
    SET isLogin = {islogin}
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    mysql.execute(SQL=sql)
    
    return

def add(**kwargs) :
    # require : store uid, table num
    return

def remove(store_uid=-1, tableNum=-1) :
    return