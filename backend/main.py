from flask import Flask
from flask_restful import Api
from flask_jwt_extended import *
from config import API
from routes import account

# flask
# pyJWT
# flask_restful
# flask_jwt_extended
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
api.add_resource(account.Get_account_info, '/get-account-info')

if __name__ == '__main__' :
    app.run(debug=True, port=API.flask_port)