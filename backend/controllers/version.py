import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import *
from statusCode import *
from flask_jwt_extended import *
from models import Admins
from models import StoreInfo
from models import TableList
from models import ProductGroup
from models import Product
from models import ProductOption
from models import ProductOptionRelations
from models import ProductSuboption
from models import OrderList
from models import SelectedOption
from models import Version

def get_version(userInputData={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in userInputData :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=userInputData["store_uid"])

    # 해당 매장이 존재하지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    versions = Version.getVersion(store["unique_store_info"])

    # 해당 매장의 버전이 존재하지 않을 때,
    if len(versions) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistVersion}

    return {"result" : "Success", "code" : Code.Success, "versions" : versions}