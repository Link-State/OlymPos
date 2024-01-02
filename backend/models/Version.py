import sys
import os
from datetime import datetime as dt
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from models import mysql
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
    disable_date = Column(DateTime, nullable=True, default=None)

    def __init__(self, store, table=None, group=None, product=None, relations=None, option=None, suboption=None, disable=None) :
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
        
        self.unique_store_info = store
        self.table_list = table
        self.product_group = group
        self.product = product
        self.product_option_relations = relations
        self.product_option = option
        self.product_suboption = suboption
        self.disable_date = disable

def getVersion(uid=-1) :
    sql = f"""
    SELECT unique_store_info, table_list, product_group, product, product_option_relations, product_option, product_suboption, disable_date
    FROM Version
    WHERE unique_store_info = {uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)
    
    # 매장 정보 없음
    if len(result) != 1 :
        return dict()
    
    # 날짜 포멧
    if result[0]["disable_date"] != None :
        date = result[0]["disable_date"].isoformat(sep=' ', timespec="seconds")
        result[0]["disable_date"] = '-'.join(date.split(':'))

    return result[0]

def setTableList(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET table_list = {time}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setProductGroup(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET product_group = {time}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setProduct(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET product = {time}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setProductOptionRelations(uid=-1, time=-1) :
    if time == -1 :
        time = datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET product_option_relations = {time}
    WHERE unique_store_info = {uid};
    """

    mysql.execute(SQL=sql)
    
    return

def setProductOption(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET product_option = {time}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def setProductSuboption(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')

    sql = f"""
    UPDATE Version
    SET product_suboption = {time}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)
    
    return

def add(uid=-1, time=datetime.datetime.now().isoformat(sep='-', timespec="milliseconds")) :
    time = time.replace(':', '').replace('-', '').replace('.', '')
    
    sql = f"""INSERT INTO Version (unique_store_info, table_list, product_group, product, product_option_relations, product_option, product_suboption, disable_date)
    VALUES('{uid}', '{time}', '{time}', '{time}', '{time}', '{time}', '{time}', NULL);"""

    mysql.execute(SQL=sql)

    return

def remove(uid=-1) :
    now = datetime.datetime.now()

    sql = f"""
    UPDATE Version
    SET disable_date = {now}
    WHERE unique_store_info = {uid};
    """
    mysql.execute(SQL=sql)

    return