import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def findUID(id="") :
    sql = f"""
    SELECT unique_admin
    FROM Admins
    WHERE user_id = '{id}';
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return -1

    return result[0]["unique_admin"]

def getUser(uid=-1) :
    result = None
    sql = f"""
    SELECT unique_admin, user_id, user_pwd, phone_number, email, disable_date
    FROM Admins
    WHERE unique_admin = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    if len(result) != 1 :
        return dict()
    
    return result[0]

def setPWD(uid=-1, pwd="") :
    
    return

def setName(uid=-1, name="") :
    
    return

def setPhoneNum(uid=-1, num="") :
    
    return

def setEmail(uid=-1, email="") :
    
    return

def add(member) :
    sql = f"""INSERT INTO Admins (user_id, user_pwd, name, phone_number, email, disable_date)
    VALUES('{member["user_id"]}', '{member["user_pwd"]}', '{member["name"]}', '{member["phone"]}', '{member["email"]}', NULL);"""

    mysql.execute(SQL=sql)
    
    return

def remove(uid=-1) :
    now = datetime.datetime.now()

    sql = f"""
    UPDATE Admins
    SET disable_date = '{now}'
    WHERE unique_admin = {uid};
    """
    mysql.execute(SQL=sql)
    
    return