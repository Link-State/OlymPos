import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
from models.mysql import DB
from sqlalchemy import Column, Integer, ForeignKey

class SelectedOption(DB.Model) :
    __tablename__ = "Selected_option"

    unique_selected_option = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_order = Column(Integer, ForeignKey('Order_list.unique_order'), nullable=False)
    unique_product_option = Column(Integer, ForeignKey('Product_option.unique_product_option'), nullable=False)
    unique_product_suboption = Column(Integer, ForeignKey('Product_suboption.unique_product_suboption'), nullable=True)

    def __init__(self, order, option, suboption=None) :
        self.unique_order = order
        self.unique_product_option = option
        self.unique_product_suboption = suboption

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