import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
