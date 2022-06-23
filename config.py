import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@127.0.0.1:8000/battery'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
