import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_jwt_extended import *
from models import Admins

def adminLogin(id="", pwd="") :
    uid = Admins.findUID(id)
    
    # 유저 아이디로 고유아이디가 검색되지 않을 때,
    if uid == -1 :
        return {"result" : "Invalid", "code" : "002"}

    user = Admins.getUser(uid)

    # 유저 아이디, 비밀번호가 맞지 않을 때,
    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "001"}
    
    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000"
    }

def userLogin(id="", pwd="", tableNum=-1) :
    uid = Admins.findUID(id)
    user = Admins.getUser(uid)

    # (관리자 계정이 존재하는지 확인할 것.)
    # 관리자 계정이 로그인 상태인지 확인할 것.
    # 해당 테이블이 존재하는지 확인할 것.
    # 해당 테이블 번호가 이미 로그인 상태인지 확인할 것.

    if "user_id" not in user or "user_pwd" not in user :
        return {"result" : "Invalid", "code" : "002"}

    if user["user_id"] != id or user["user_pwd"] != pwd :
        return {"result" : "Invalid", "code" : "001"}
        
    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : "000"
    }

def adminLogout(id="", pwd="", tableNum=-1) :
    if (id == "asdf" and pwd == "1234") :
        return {"result" : "Success"}
    else :
        return {"result" : "Invalid"}

def userLogout(id="", pwd="", tableNum=-1) :

    if (id == "asdf" and pwd == "1234") :
        return {"result" : "Success"}
    else :
        return {"result" : "Invalid"}

def signup() :
    return

def delete_account() :
    return