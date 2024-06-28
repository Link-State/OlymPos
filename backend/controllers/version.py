import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import *
from statusCode import *
from flask_jwt_extended import *
from models import StoreInfo
from models import Version

def get_version(userInputData={}) :
    # 필수 값이 누락됐을 때,
    if "store_uid" not in userInputData :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    store = StoreInfo.getStore(uid=userInputData["store_uid"])

    # 매장이 존재하지 않을 때,
    if len(store) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    versions = Version.getVersion(uid=store["unique_store_info"])

    if len(versions) <= 0 :
        return {"result" : "Invalid", "code" : Code.NotExistVersion}

    return {"result" : "Success", "code" : Code.Success, "versions" : versions}