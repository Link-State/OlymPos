import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, ForeignKey

class ProductOptionRelations(DB.Model) :
    __tablename__ = "Product_Option_relations"

    unique_product = Column(Integer, ForeignKey('Product.unique_product'), primary_key=True, nullable=False)
    unique_product_option = Column(Integer, ForeignKey('Product_option.unique_product_option'), primary_key=True, nullable=False)

    def __init__(self, product, option) :
        self.unique_product = product
        self.unique_product_option = option
