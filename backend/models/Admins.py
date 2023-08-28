import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
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
    sql = f"""
    UPDATE Admins
    SET user_pwd = '{pwd}'
    WHERE unique_admin = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setName(uid=-1, name="") :
    sql = f"""
    UPDATE Admins
    SET name = '{name}'
    WHERE unique_admin = {uid};
    """
    mysql.execute(SQL=sql)

    return

def setPhoneNum(uid=-1, num="") :
    sql = f"""
    UPDATE Admins
    SET phone_number = '{num}'
    WHERE unique_admin = {uid};
    """
    mysql.execute(SQL=sql)

    return

def setEmail(uid=-1, email="") :
    sql = f"""
    UPDATE Admins
    SET email = '{email}'
    WHERE unique_admin = {uid};
    """

    mysql.execute(SQL=sql)

    return

def add(userData) :
    sql = f"""INSERT INTO Admins (user_id, user_pwd, name, phone_number, email, disable_date)
    VALUES('{userData["user_id"]}', '{userData["user_pwd"]}', '{userData["name"]}', '{userData["phone"]}', '{userData["email"]}', NULL);"""

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