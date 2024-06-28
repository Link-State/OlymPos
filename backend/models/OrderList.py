import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, DateTime, ForeignKey

class OrderList(DB.Model) :
    __tablename__ = "Order_list"

    unique_order = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    unique_product = Column(Integer, ForeignKey('Product.unique_product'), nullable=False)
    table_number = Column(Integer, ForeignKey('Table_list.table_number'), nullable=True)
    amount = Column(Integer, nullable=False)
    order_state = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    last_modify_date = Column(DateTime, nullable=False)

    def __init__(self, store, product, amount, state, date, last, number=None) :
        self.unique_store_info = store
        self.unique_product = product
        self.table_number = number
        self.amount = amount
        self.order_state = state
        self.order_date = date
        self.last_modify_date = last
