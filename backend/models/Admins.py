import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from models.mysql import DB
from sqlalchemy import Column, Integer, String, DateTime

class Admins(DB.Model) :
    __tablename__ = "Admins"

    unique_admin = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(String(MaxLength.user_id), nullable=False)
    user_pwd = Column(String(MaxLength.user_pwd), nullable=False)
    name = Column(String(MaxLength.user_name), nullable=False)
    phone_number = Column(String(MaxLength.phone_number), nullable=False)
    email = Column(String(MaxLength.email), nullable=False)
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, id, pwd, name, number, email, disable=None) :
        self.user_id = id
        self.user_pwd = pwd
        self.name = name
        self.phone_number = number
        self.email = email
        self.disable_date = disable
