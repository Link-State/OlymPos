from flask import Flask
from flask_restful import Api
from flask_jwt_extended import *
from flask_cors import CORS
from config import API
from routes import account
from routes import store
from routes import product
from routes import version

# flask
# pyJWT
# flask_restful
# flask_jwt_extended
# flask_cors
# pymysql
# cryptography

connection = None
command = None

app = Flask(import_name=__name__)
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = API.key
)

jwt = JWTManager(app)

api = Api(app)
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
api.add_resource(product.Get_group_list, '/get-group-list')
api.add_resource(product.Get_product_list, '/get-product-list')
api.add_resource(product.Get_option_list, '/get-option-list')

api.add_resource(version.Get_store_version, '/get-store-version')

cors = CORS(app, resources={r'*' : {'origins' : '*'}})

if __name__ == '__main__' :
    app.run(debug=True, port=API.flask_port)