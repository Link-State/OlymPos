import sys
import os

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
    # uid, id, pwd, name, phone num, email, islogin
    # 프론트엔드로 output시 pwd, islogin 정보는 지워서 output
    result = None
    sql = f"""
    SELECT unique_admin, user_id, user_pwd, phone_number, email, isLogin
    FROM Admins
    WHERE user_id = {uid};
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

def setIsLogin(uid=-1, islogin=0) :
    sql = f"""
    UPDATE Admins
    SET isLogin = 1
    WHERE unique_admin = {uid};
    """

    mysql.execute(SQL=sql)
    
    return

def add(**kwargs) :
    # id, pwd, name, phone num, email
    return

def remove(uid=-1) :
    
    return