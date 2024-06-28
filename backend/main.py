import os

from flask import Flask, render_template, redirect, request
from flask_restful import Api
from flask_jwt_extended import *
from flask_cors import CORS
from config import API
from utils import Path
from routes import account
from routes import store
from routes import product
from routes import order
from routes import version
from models.mysql import DB

# flask
# flask_restful
# flask_jwt_extended
# flask_cors
# flask_sqlalchemy
# pyJWT
# pymysql
# cryptography
# pillow

# 이미지 폴더 생성
if not os.path.exists(Path.ADMIN) :
    os.makedirs(Path.ADMIN)

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

@app.route('/test', methods=['GET'])
def test() :
    data = dict()
    return render_template('test.html', data=data)

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
api.add_resource(account.Find_password, '/find-password')

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