import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class StoreInfo(DB.Model) :
    __tablename__ = "Store_info"

    unique_store_info = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    unique_admin = Column(Integer, ForeignKey('Admins.unique_admin'), nullable=False)
    store_name = Column(String(MaxLength.store_name), nullable=False)
    store_owner = Column(String(MaxLength.store_owner), nullable=False)
    store_address = Column(String(MaxLength.store_address), nullable=False)
    store_tel_number = Column(String(MaxLength.store_tel_number), nullable=False)
    table_count = Column(Integer, nullable=False)
    last_modify_date = Column(DateTime, nullable=True, default=None)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, admin, name, owner, address, number, count, last=None, disable=None) :
        self.unique_admin = admin
        self.store_name = name
        self.store_owner = owner
        self.store_address = address
        self.store_tel_number = number
        self.table_count = count
        if last == None :
            self.last_modify_date = datetime.now()
        else :
            self.last_modify_date = last
        self.disable_date = disable
