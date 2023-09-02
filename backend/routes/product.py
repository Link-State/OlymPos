import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from statusCode import *
from flask import request, jsonify, session
from flask_jwt_extended import *
from flask_restful import Resource
from controllers import product

class Add_group(Resource) :
    @jwt_required()
    def post(self) :
        return

class Modify_group(Resource) :
    @jwt_required()
    def post(self) :
        return

class Delete_group(Resource) :
    @jwt_required()
    def post(self) :
        return

class Add_product(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Modify_product(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Delete_product(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Add_option(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Modify_option(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Delete_option(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Add_suboption(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Modify_suboption(Resource) :
    @jwt_required()
    def post(self) :
        return
    
class Delete_suboption(Resource) :
    @jwt_required()
    def post(self) :
        return

class Get_group_list(Resource) :
    @jwt_required()
    def get(self) :
        return

class Get_product_list(Resource) :
    @jwt_required()
    def get(self) :
        return
    
class Get_option_list(Resource) :
    @jwt_required()
    def get(self) :
        return