import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

# 해당 매장의 주문 목록 반환
def getOrders(store_id=-1) :
    return

def getOrder(uid=-1) :
    return

def setProduct(uid=-1, product_id=-1) :
    return

def setTableNum(uid=-1, num=-1) :
    return

def setAmount(uid=-1, amount=-1) :
    return

def setState(uid=-1, state=0) :
    return

def setDate(uid=-1, date=datetime.datetime.today()) :
    return

def add(**kwargs) :
    # require : store id, product id, table num, amount
    return

def remove(uid=-1) :
    return
