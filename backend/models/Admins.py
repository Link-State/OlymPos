import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
from models.mysql import DB
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql.schema import Column

# models/* 각 파일에 아래와 같은 테이블 클래스 선언하여 사용하는 방향으로 가야함.
class Admins(DB.Model) :
    __tablename__ = "Admins"

    unique_admin = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(String(MaxLength.user_id), nullable=False)
    user_pwd = Column(String(MaxLength.user_pwd), nullable=False)
    name = Column(String(MaxLength.user_name), nullable=False)
    phone_number = Column(String(MaxLength.phone_number), nullable=False)
    email = Column(String(MaxLength.email), nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, id, pwd, name, number, email, disable=None) :
        self.user_id = id
        self.user_pwd = pwd
        self.name = name
        self.phone_number = number
        self.email = email
        self.disable_date = disable

def findUID(id="") :
    sql = f"""
    SELECT unique_admin
    FROM Admins
    WHERE user_id = '{id}';
    """

    result = mysql.execute(SQL=sql, fetch=True)

    # 해당 아이디의 유저를 찾을 수 없음
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

    # 해당 유저 찾을 수 없음
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