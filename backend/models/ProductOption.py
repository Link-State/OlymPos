import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ProductOption(DB.Model) :
    __tablename__ = "Product_option"

    unique_product_option = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    option_name = Column(String(MaxLength.option_name), nullable=False)
    price = Column(Integer, nullable=False)
    suboption_offer = Column(Integer, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, name, price, offer, disable=None) :
        self.unique_store_info = store
        self.option_name = name
        self.price = price
        self.suboption_offer = offer
        self.disable_date = disable
