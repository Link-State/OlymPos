import os
import sys

from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import API
from config import Path
from config import MaxLength
from routes import account
from routes import store
from routes import product
from routes import order
from routes import version
from models.mysql import DB
from models.Admins import Admins
from models.StoreInfo import StoreInfo

# flask
# flask_restful
# flask_jwt_extended
# flask_cors
# flask_sqlalchemy
# pyJWT
# pymysql
# cryptography

# 이미지 폴더 생성
if not os.path.exists(Path.IMAGE) :
    os.mkdir(Path.IMAGE)

# 안쓰는 변수(삭제할 것)
connection = None
command = None

app = Flask(import_name=__name__)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = API.key
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{API.mysql_username}:{API.mysql_pwd}@{API.host}:{API.mysql_port}/{API.database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy()를 두번 호출하면 오류남.
# db = SQLAlchemy()를 호출한 모듈이 완전히 초기화 된 후 다른 곳에서 db변수를 불러와야 함.
# https://streamls.tistory.com/entry/Flask%EA%B0%95%EC%A2%8C4-FlaskSQLAlchemy-Database%EC%97%B0%EB%8F%99
DB.init_app(app)

jwt = JWTManager(app)

api = Api(app)

@app.route('/test')
def test() :
    print("hello\n\n\n\n\n")
    
    # 추가
    admin = Admins(id="test1", pwd="test1", name="dummy", number="01012341234", email="asdf@qwer.com")
    DB.session.add(admin)
    DB.session.commit()

    aaaa = Admins.query.all()

    for i in aaaa :
        print(i.unique_admin)
        print(i.user_id)
        print(i.user_pwd)
        print(i.name)
        print(i.phone_number)
        print(i.email)
        print(i.disable_date)
        print()

    store = StoreInfo(admin=admin.unique_admin, name="우하하 가게", owner="칡칡이", address="음메민국 칡소시 발굽로 123-2", number="033-123-3333", count=4)
    DB.session.add(store)
    DB.session.commit()

    bbbb = StoreInfo.query.all()

    for i in bbbb :
        print(i.unique_store_info)
        print(i.unique_admin)
        print(i.store_name)
        print(i.store_owner)
        print(i.store_address)
        print(i.store_tel_number)
        print(i.table_count)
        print(i.last_modify_date)
        print(i.disable_date)
        print()

    # 삭제
    admin = Admins.query.filter_by(name="dummy")

    if admin.count() == 1 :
        DB.session.delete(admin.first())
        DB.session.commit()

    store = StoreInfo.query.filter_by(store_name="우하하 가게")

    if store.count() == 1 :
        DB.session.delete(store.first())
        DB.session.commit()

    print("\n\n\n\n\n")
    print("hello world")

api.add_resource(account.AdminLogin, '/admin-login')
api.add_resource(account.AdminLogout, '/admin-logout')
api.add_resource(account.UserLogin, '/user-login')
api.add_resource(account.TableLogin, '/table-login')
api.add_resource(account.UserLogout, '/user-logout')
api.add_resource(account.Signup, '/signup')
api.add_resource(account.Delete_account, '/delete-account')
api.add_resource(account.Change_account_info, '/change-account-info')
api.add_resource(account.Get_exist_user, '/get-exist-user')
api.add_resource(account.Get_account_info, '/get-account-info')
api.add_resource(account.Find_account, '/find-account')

api.add_resource(store.Add_store, '/add-store')
api.add_resource(store.Change_store_info, '/change-store-info')
api.add_resource(store.Delete_store, '/delete-store')
api.add_resource(store.Get_my_stores, '/get-my-stores')
api.add_resource(store.Get_store_info, '/get-store-info')

api.add_resource(product.Add_group, '/add-product-group')
api.add_resource(product.Modify_group, '/modify-product-group')
api.add_resource(product.Delete_group, '/delete-product-group')
api.add_resource(product.Add_product, '/add-product')
api.add_resource(product.Modify_product, '/modify-product')
api.add_resource(product.Delete_product, '/delete-product')
api.add_resource(product.Add_option, '/add-product-option')
api.add_resource(product.Modify_option, '/modify-product-option')
api.add_resource(product.Delete_option, '/delete-product-option')
api.add_resource(product.Add_suboption, '/add-product-suboption')
api.add_resource(product.Modify_suboption, '/modify-product-suboption')
api.add_resource(product.Delete_suboption, '/delete-product-suboption')
api.add_resource(product.Modify_product_option_relation, '/modify-product-option-relation')
api.add_resource(product.Get_group_list, '/get-group-list')
api.add_resource(product.Get_product_list, '/get-product-list')
api.add_resource(product.Get_option_list, '/get-option-list')

api.add_resource(order.Product_order, '/product-order')
api.add_resource(order.Change_order_state, '/change-order-state')
api.add_resource(order.Change_table_state, '/change-table-state')
api.add_resource(order.Get_order_list, '/get-order-list')
api.add_resource(order.Get_table_list, '/get-table-list')

api.add_resource(version.Get_store_version, '/get-store-version')

cors = CORS(app, resources={r'*' : {'origins' : '*'}})

if __name__ == '__main__' :
    app.run(debug=True, port=API.flask_port)