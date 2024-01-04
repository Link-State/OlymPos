import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models.mysql import DB
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

class TableList(DB.Model) :
    __tablename__ = "Table_list"

    unique_store_info = Column(Integer, ForeignKey('Store_info.unique_store_info'), primary_key=True, nullable=False)
    table_number = Column(Integer, primary_key=True, nullable=False)
    table_state = Column(Integer, nullable=False)
    isLogin = Column(Text, nullable=False, default="")
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, number, state, login="", disable=None) :
        self.unique_store_info = store
        self.table_number = number
        self.table_state = state
        self.isLogin = login
        self.disable_date = disable
