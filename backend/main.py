import pymysql
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import *
from config import API
from routes import account

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
api.add_resource(account.UserLogout, '/user-logout')
api.add_resource(account.Signup, '/signup')

if __name__ == '__main__' :
    # host를 127.0.0.1로 바꿔도 작동이 될까?
    # connection = pymysql.connect(host=API.host, user=API.mysql_username, password=API.mysql_pwd, database=API.database, port=API.mysql_port, use_unicode=True, charset="utf8")
    # command = connection.cursor()
    app.run(debug=True, port=API.flask_port)