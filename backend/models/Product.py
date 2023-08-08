import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import connection, command

# 해당 매장의 모든 상품 목록 반환
def getProducts(store_uid=-1) :
    return

def getProduct(uid=-1) :
    return

def setStore(uid=-1, id=-1) :
    return

def setGroupID(uid=-1, id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setImage(uid=-1, image="") :
    return

def setDescription(uid=-1, descript="") :
    return

def setAmount(uid=-1, amount=-1) :
    return

def add(**kwargs) :
    # require : group uid, name, price
    return

def remove(uid=-1) :
    return