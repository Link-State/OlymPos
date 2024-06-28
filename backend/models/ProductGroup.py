import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ProductGroup(DB.Model) :
    __tablename__ = "Product_group"

    unique_product_group = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), nullable=False)
    group_name = Column(String(MaxLength.group_name), nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, name, disable=None) :
        self.unique_store_info = store
        self.group_name = name
        self.disable_date = disable
