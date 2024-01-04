import sys
import os
from datetime import datetime as dt

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey

class Version(DB.Model) :
    __tablename__ = "Version"

    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), primary_key=True, nullable=False)
    table_list = Column(BigInteger, nullable=False)
    product_group = Column(BigInteger, nullable=False)
    product = Column(BigInteger, nullable=False)
    product_option_relations = Column(BigInteger, nullable=False)
    product_option = Column(BigInteger, nullable=False)
    product_suboption = Column(BigInteger, nullable=False)
    order_list = Column(BigInteger, nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, table=None, group=None, product=None, relations=None, option=None, suboption=None, order=None, disable=None) :
        now = int(dt.now().strftime('%Y%m%d%H%M%S%f')[:-3])

        if table == None :
            table = now
        if group == None :
            group = now
        if product == None :
            product = now
        if relations == None :
            relations = now
        if option == None :
            option = now
        if suboption == None :
            suboption = now
        if order == None :
            order = now
        
        self.unique_store_info = store
        self.table_list = table
        self.product_group = group
        self.product = product
        self.product_option_relations = relations
        self.product_option = option
        self.product_suboption = suboption
        self.order_list = order
        self.disable_date = disable
