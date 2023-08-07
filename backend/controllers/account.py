import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_jwt_extended import *
from helpers import account

# 관리자 / 사용자 로그인 구분?
def adminLogin(id="", pwd="") :
    # 아이디를 key로 유저 정보 받아옴
    # 받아온 유저 정보가 요청한 유저 정보와 일치하면 로그인
    user = account.getUser()
    if (user["id"] == id and user["pwd"] == pwd) :
        return {"result" : "Success",
            "access_token" : create_access_token(identity=id, expires_delta=False)
        }
    else :
        return {"result" : "Invalid"}

def userLogin(id="", pwd="", tableNum=-1) :
    user = account.getUser()
    if (user["id"] == id and user["pwd"] == pwd) :
        return {"result" : "Success",
            "access_token" : create_access_token(identity=id, expires_delta=False)
        }
    else :
        return {"result" : "Invalid"}

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