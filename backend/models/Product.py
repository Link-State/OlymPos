import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import mysql

def getProducts(store_uid=-1, include_disable=False) :
    select = ''
    where = " and disable_date is NULL"

    if include_disable :
        select = ", disable_date"
        where = ''
    
    sql = f"""
    SELECT unique_product, unique_store_info, unique_product_group, product_name, price, image, description, amount{select}
    FROM Product
    WHERE unique_store_info = {store_uid}{where};
    """

    return mysql.execute(SQL=sql, fetch=True)

def getProduct(uid=-1) :
    return

def setStore(uid=-1, id=-1) :
    return

def setGroupID(uid=-1, id=-1) :
    return

def setName(uid=-1, name="") :
    return

def setPrice(uid=-1, price=0) :
    return

def setImage(uid=-1, image="") :
    return

def setDescription(uid=-1, descript="") :
    return

def setAmount(uid=-1, amount=-1) :
    return

def add(**kwargs) :
    # require : group uid, name, price
    return

def remove(uid=-1) :
    return