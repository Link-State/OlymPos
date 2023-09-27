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

def product_order(userInputData={}) :
    # 필수 필드가 누락 됐을 때,
    # 주문을 시도한 기기의 SSAID, 주문을 시도한 테이블의 isLogin DB값과 같은지 체크
    # 존재하지 않는 매장일 때,
    # 존재하지 않는 상품일 때,
    # 존재하지 않는 테이블 번호일 때,
    # 1. 선택한 옵션이 List 형식이 아닐 때,
    # 2. 선택한 옵션의 List의 원소(=옵션 및 서브옵션)가 Dict가 아닐 때
    # 3. 선택한 옵션의 List의 원소(=옵션 및 서브옵션)가 존재하지 않는 옵션, 서브옵션일 때,
    return