import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def getOption(product_uid=-1, option_uid=-1) :
    return

def getOptions(product_uid=-1) :
    sql = f"""
    SELECT unique_product_option
    FROM Product_Option_relations
    WHERE unique_product = {product_uid};
    """

    result = mysql.execute(SQL=sql, fetch=True)

    options = []
    for rec in result :
        options.append(rec["unique_product_option"])

    return options

def add(product_uid=-1, option_uid=-1) :
    sql = f"""INSERT INTO Product_Option_relations (unique_product, unique_product_option)
    VALUES('{product_uid}', '{option_uid}');"""

    mysql.execute(SQL=sql)

    # 생성됐는지 검사

    return

def remove(product_uid=-1, option_uid=-1) :
    sql = f"""
    DELETE FROM Product_Option_relations
    WHERE unique_product = {product_uid} and unique_product_option = {option_uid};
    """

    mysql.execute(SQL=sql)

    # 삭제 됐는지 검사
    return