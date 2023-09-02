import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

# 해당 옵션의 서브옵션 목록 반환
def getSubOptions(option_id=-1) :
    return

def getSubOption(uid=-1) :
    return

def setOption(uid=-1, option_id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setAmount(uid=-1, amount=-1) :
    return

def add(**kwargs) :
    # require : product id, name, price, amount
    return

def remove(uid=-1) :
    return