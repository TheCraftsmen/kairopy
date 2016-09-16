from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime


class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(64))
    token = db.Column(db.String(128), default='')
    email = db.Column(db.String(128), nullable=False)
    request_list = relationship("RequestList", backref="user")
    request_settings = relationship("UserSettings", backref="user")
    validate = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(10), default='user')
    user_offers = relationship("UserOffer", backref="user")
    user_role = db.Column(db.String(10), default='customer')

    def __init__(self, name, email, password, user_role):
        self.username = name
        self.email = email
        self.hash_password(password)
        self.user_role = user_role

    def get_name(self):
        return self.username

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def getUserId(self):
        return self.id

    def setToken(self, token):
        self.token = token

    def getToken(self):
        try:
            print self.token
            return unicode(self.token)  # python 2
        except NameError:
            print self.token
            return str(self.token)  # python 3

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<name {}'.format(self.username)


class RequestList(db.Model):

    __tablename__ = "requestList"

    table_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    request_date = db.Column(db.Date, default=datetime.date.today())
    cust_name = db.Column(db.String(50), nullable=True)
    request_type = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, custname, request_type, status, number, user_id):
        self.cust_name = custname
        self.status = status
        self.number = number
        self.user_id = user_id
        self.request_type = request_type

    def __repr__(self):
        pass

class UserSettings(db.Model):

    __tablename__ = "userSettings"

    table_id = db.Column(db.Integer, primary_key=True)
    column_turn = db.Column(db.String(20), default='Posicion')
    column_custname = db.Column(db.String(20), default='Nombre')
    column_type = db.Column(db.String(20), default='Descripcion')
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        pass

class UserOffer(db.Model):
    """docstring for UserOffer"""

    __tablename__ = "user_offers"

    table_id = db.Column(db.Integer, primary_key=True)
    offer_name = db.Column(db.String(20))
    offer_discount = db.Column(db.String(20))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, user_id, offer_name, offer_discount):
        self.user_id = user_id
        self.offer_name = offer_name
        self.offer_discount = offer_discount

    @classmethod
    def getOffersforUser(self, user_id):
        return self.query.filter_by(user_id=user_id)