import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ProductSuboption(DB.Model) :
    __tablename__ = "Product_suboption"

    unique_product_suboption = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_product_option = Column(Integer, ForeignKey('Product_option.unique_product_option'), nullable=False)
    suboption_name = Column(String(MaxLength.suboption_name), nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, option, name, price, amount, disable=None) :
        self.unique_product_option = option
        self.suboption_name = name
        self.price = price
        self.amount = amount
        self.disable_date = disable
