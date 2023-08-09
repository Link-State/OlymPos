import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import connection, command

# 해당 주문의 모든 옵션 목록을 반환
def getOptions(order_id=-1) :
    return

def getOption(uid=-1) :
    return

def setOption(uid=-1, option_id=-1) :
    return

def setSubOption(uid=-1, suboption_id=-1) :
    return

def add(**kwargs) :
    # require : order id, option id, suboption id
    return

def remove(uid=-1) :
    return