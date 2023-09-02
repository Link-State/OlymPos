import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql

# 해당 매장의 카테고리 목록 반환
def getGroups(store_id=-1) :
    # uid, name
    return

def setGroup(uid=-1, name="") :
    return

def add(**kwargs) :
    # require : store uid, group name
    return

def remove(uid=-1) :
    return