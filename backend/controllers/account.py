import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_jwt_extended import *
from models import Admins

def adminLogin(id="", pwd="") :
    uid = Admins.findUID()
    user = Admins.getUser(uid)

    if (user["id"] == id and user["pwd"] == pwd) :
        return {"result" : "Success",
            "access_token" : create_access_token(identity=id, expires_delta=False)
        }
    else :
        return {"result" : "Invalid"}

def userLogin(id="", pwd="", tableNum=-1) :
    user = Admins.getUser()
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