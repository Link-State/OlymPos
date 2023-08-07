import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import connection, command

# 해당 관리자의 매장 목록 반환
def getStores(admin_id=-1) :
    return

def getStore(uid=-1) :
    # uid, admin uid, name, owner, address, tel num
    if uid < 0 :
        return
    
    return

def setAdminUID(uid=-1, admin_uid=-1) :
    return

def setName(uid=-1, name="") :
    return

def setOwner(uid=-1, owner="") :
    return

def setAddress(uid=-1, address="") :
    return

def setTelNum(uid=-1, num="") :
    return

def add(**kwargs) :
    # admin uid, name, owner, address, tel num
    return

def remove(uid=-1) :
    return