import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

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