import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "my precious"
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "sqlite:///kairopy.db"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:fuckblas3345@localhost/kairopy"
    RECAPTCHA_PUBLIC_KEY = '6LdQlgcUAAAAAEMpv3th2TAGkqUpnAT2hiLJIiXa'
    RECAPTCHA_PRIVATE_KEY = '6LdQlgcUAAAAAGBaVUxKhINMWB5b32jl8q42zDlN'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
