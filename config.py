import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "my precious"
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "sqlite:///kairopy.db"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:fuckblas3345@localhost/kairopy"

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
