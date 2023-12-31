import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql
from models.mysql import DB
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, Text, DateTime, ForeignKey

class TableList(DB.Model) :
    __tablename__ = "Table_list"

    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'))
    table_number = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    table_state = Column(Integer, nullable=False)
    isLogin = Column(Text, nullable=False, default="")
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, number, state, login="", disable=None) :
        self.table_number = number
        self.table_state = state
        self.isLogin = login
        self.disable_date = disable


def getTables(store_uid=-1) :
    sql = f"""
    SELECT unique_store_info, table_number, table_state, isLogin, disable_date
    FROM Table_list
    WHERE unique_store_info = {store_uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    # 각 테이블에 대한 날짜 포맷팅
    for st in result :
        if st["disable_date"] != None :
            date = st["disable_date"].isoformat(sep=' ', timespec="seconds")
            st["disable_date"] = '-'.join(date.split(':'))

    return result

def getTable(store_uid=-1, tableNum=-1) :
    sql = f"""
    SELECT unique_store_info, table_number, table_state, isLogin, disable_date
    FROM Table_list
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 해당 테이블 없음
    if len(result) != 1 :
        return dict()

    # 날짜 포맷
    if result[0]["disable_date"] != None :
        date = result[0]["disable_date"].isoformat(sep=' ', timespec="seconds")
        result[0]["disable_date"] = '-'.join(date.split(':'))

    return result[0]

def setTableNum(store_uid=-1, tableNum=-1) :
    return

def setState(store_uid=-1, tableNum=-1, state=-1) :
    sql = f"""
    UPDATE Table_list
    SET table_state = {state}
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    mysql.execute(SQL=sql)

    return

def setIsLogin(store_uid=-1, tableNum=-1, islogin='') :
    sql = f"""
    UPDATE Table_list
    SET isLogin = '{islogin}'
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    mysql.execute(SQL=sql)
    
    return

def add(userData) :
    sql = f"""INSERT INTO Table_list (unique_store_info, table_number, table_state, isLogin, disable_date)
    VALUES('{userData["store_uid"]}', '{userData["table"]}', 0, '', NULL);"""

    mysql.execute(SQL=sql)

    return

def remove(store_uid=-1, tableNum=-1) :
    now = datetime.datetime.now()

    sql = f"""
    UPDATE Table_list
    SET disable_date = '{now}'
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    mysql.execute(SQL=sql)
    return

def restore(store_uid=-1, tableNum=-1) :
    sql = f"""
    UPDATE Table_list
    SET disable_date = NULL
    WHERE unique_store_info = {store_uid} and table_number = {tableNum};
    """

    mysql.execute(SQL=sql)
    
    return