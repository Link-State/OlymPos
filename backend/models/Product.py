import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey

class Product(DB.Model) :
    __tablename__ = "Product"

    unique_product = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    unique_product_group = Column(Integer, ForeignKey('Product_group.unique_product_group'), nullable=False)
    product_name = Column(String(MaxLength.product_name), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(Text, nullable=True, default="")
    description = Column(Text, nullable=True, default="")
    amount = Column(Integer, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, group, name, price, amount, disable=None, img="", descrp="") :
        self.unique_store_info = store
        self.unique_product_group = group
        self.product_name = name
        self.price = price
        self.image = img
        self.description = descrp
        self.amount = amount
        self.disable_date = disable
