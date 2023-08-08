import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def findUID(id="") :
    return

def getUser(uid=-1) :
    # uid, id, pwd, name, phone num, email, islogin
    # 프론트엔드로 output시 pwd, islogin 정보는 지워서 output
    
    return

def setPWD(uid=-1, pwd="") :
    
    return

def setName(uid=-1, name="") :
    
    return

def setPhoneNum(uid=-1, num="") :
    
    return

def setEmail(uid=-1, email="") :
    
    return

def setIsLogin(uid=-1, islogin=0) :
    
    return

def add(**kwargs) :
    # id, pwd, name, phone num, email
    return

def remove(uid=-1) :
    
    return