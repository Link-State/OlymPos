import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from statusCode import *
from flask import request, jsonify, session
from flask_jwt_extended import *
from flask_restful import Resource
from controllers import version

class Get_store_version(Resource) :
    def get(self) :
        user_data = request.args.to_dict()
        return jsonify(version.get_version(userInputData=user_data))
