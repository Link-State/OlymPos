import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, DateTime, ForeignKey

class SelectedOption(DB.Model) :
    __tablename__ = "Selected_option"

    unique_selected_option = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_order = Column(Integer, ForeignKey('Order_list.unique_order'), nullable=False)
    unique_product_option = Column(Integer, ForeignKey('Product_option.unique_product_option'), nullable=False)
    unique_product_suboption = Column(Integer, ForeignKey('Product_suboption.unique_product_suboption'), nullable=True)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, order, option, suboption=None, disable=None) :
        self.unique_order = order
        self.unique_product_option = option
        self.unique_product_suboption = suboption
        self.disable_date = disable