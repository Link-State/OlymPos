import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import connection, command

# 해당 제품의 옵션 목록 반환
def getOptions(product_uid=-1) :
    return

def getOption(uid=-1) :
    return

def setStore(uid=-1, id=-1) :
    return

def setProduct(uid=-1, product_id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setIsOffer(uid=-1, isoffer=0) :
    return

def add(**kwargs) :
    # require : product id, name, price, isOffer
    return

def remove(uid=-1) :
    return