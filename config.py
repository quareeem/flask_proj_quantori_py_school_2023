import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
 
SQLALCHEMY_DATABASE_URI = 'sqlite:///blogc.db' 
SECRET_KEY = 'mf'