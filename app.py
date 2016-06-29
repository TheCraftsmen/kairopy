#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, abort, request, jsonify, g, url_for, render_template, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask_mail import Mail, Message
from flask_restful import Resource, Api
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user

from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView

import datetime
import time
import sys

app = Flask(__name__)
app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'kairopy@gmail.com',
    MAIL_PASSWORD = 'NothingGonnaChange'
)

mail = Mail(app)


# initialization
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object('config.ProductionConfig')
api = Api(app)
# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
from models import *
from forms import LoginForm, LogupForm, ResetForm

login_manager.login_view = "login"



class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        if current_user.role == 'admin':
            return super(MyAdminIndexView, self).index()
        else:
            return redirect(url_for('index'))


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(RequestList, db.session))
admin.add_view(ModelView(UserSettings, db.session))

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

'''
'''
from rest.allrest import AllTurn, UpdateStatus, ChangeSettings, CleanAll
api.add_resource(AllTurn, '/_all_turn/<int:user_id>')
api.add_resource(CleanAll, '/_clean_all/<int:user_id>')
api.add_resource(UpdateStatus, '/_update_status/<int:api_num>/<int:user>')
api.add_resource(ChangeSettings, '/_change_settings/<int:user_id>/<string:column_name>/<string:new_value>')

@app.route('/request', methods=['GET', 'POST'])
@login_required
def request_view():
    from models import RequestList
    lastNumber = False
    lastDate = False
    lastStatus = False
    print(current_user.get_name())
    queryA = RequestList.query.filter_by(user_id=current_user.get_id()).order_by(RequestList.table_id.desc()).limit(1)
    for row in queryA:
        lastDate = row.request_date
        lastNumber = row.number
        lastStatus = row.status
    pNumber = 1
    pStatus = 1
    if lastDate == datetime.date.today():
        pNumber = lastNumber + 1
        if lastStatus and lastStatus == 2:
            pStatus = 1
        else:
            pStatus = 0
    if request.method == 'POST':
        if request.form['cust_name']:
            rl = RequestList(
            custname=request.form['cust_name'].upper(),
            request_type=request.form['request_type'].upper(),
            status=pStatus,
            number=pNumber,
            user_id=current_user.get_id())
            db.session.add(rl)
            db.session.commit()
    return render_template('request.html')


@app.route('/monitor')
@login_required
def monitor():
    return render_template('monitor.html')


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


@app.route('/logup', methods=['GET','POST'])
def logup():
    error = None
    form = LogupForm()

    if request.method == 'POST' and form.validate_on_submit():
        usertest = User.query.filter_by(email=form.email.data).first()
        if usertest: return render_template('logup.html', form=form, error=error)
        if form.password.data == form.repeatpassword.data:
            db.session.add(User(
            form.username.data,
            form.email.data, 
            form.password.data))
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
            db.session.add(UserSettings(user.id))
            db.session.commit()

            token = user.generate_auth_token(600)
            user.setToken(token)
            db.session.commit()
            msg = Message("Bienvenido a Kairopy",
                  sender="kairopy@gmail.com",
                  recipients=[user.email])
            msg.html = render_template("validate-email.html", username=user.username, link="www.kairopy.com/validateemail/%s/%s" % (user.id, token))
            mail.send(msg)
            return "Revisa en tu Correo el Mensaje de Validacion"
        else:
            error = u"Los Passwords No Coinciden"
    return render_template('logup.html', form=form, error=error)


@app.route('/reset', methods=['GET','POST'])
def reset():
    error = None
    form = ResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.username.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                token = user.generate_auth_token(600)
                print token
                user.setToken(token)
                db.session.commit()
                msg = Message("Recuperacion de Credenciales",
                      sender="kairopy@gmail.com",
                      recipients=[user.email])
                msg.html = render_template("reset-password.html", username=user.username, link="www.kairopy.com/changepassword/%s/%s" % (user.id, token))
                mail.send(msg)
                flash("Mensaje Enviado")
                return redirect(url_for('login'))
            else:
                error = u"No Existe el Usuario"
        else:
            error = u"No Cargo Usuario"
    return render_template('reset.html', form=form, error=error)


@app.route('/changepassword/<int:user_id>/<string:token>', methods=['GET','POST'])
def changepassword(user_id, token):
    if request.method == 'POST':
        user = User.query.filter_by(id=request.form['user_id']).first()
        if user and request.form['password'] == request.form['repeatpassword']:
            user.hash_password(request.form['password'])
            db.session.commit()
            return redirect(url_for('login'))
    user = User.query.filter_by(id=user_id).first()
    if user and user.token == token:
        return render_template("change.html", user_id=user_id)
    return "Acceso Denegado"

@app.route('/validateemail/<int:user_id>/<string:token>', methods=['GET','POST'])
def validateemail(user_id, token):
    user = User.query.filter_by(id=user_id).first()
    if user and user.token == token and not user.validate:
        user.validate = True
        db.session.commit()
        return "Ahora Puede Ingresar a Kairopy"
    else:
        return "Acceso Denegado"


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    g.user.setToken(token)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/')
@login_required
def index():
    process = RequestList.query.filter_by(status= 2).filter_by(user_id=current_user.id).filter(RequestList.request_date >=datetime.date.today()).count()
    pending = RequestList.query.filter(RequestList.status.in_((0, 1))).filter_by(user_id=current_user.id).filter(RequestList.request_date >=datetime.date.today()).count()
    totalToday = RequestList.query.filter_by(user_id=current_user.id).filter(RequestList.request_date >=datetime.date.today()).count()
    history = RequestList.query.filter_by(user_id=current_user.id).count()
    return render_template("index.html", 
        querydata=['Procesados', 'Pendientes', 'Total Diario', 'Historico'],
        dictdata={'Procesados':process, 
        'Pendientes':pending, 
        'Total Diario':totalToday, 
        'Historico':history} )

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("entra")
    error = None
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and pwd_context.verify(form.password.data, user.password) and user.validate:
            login_user(user)
            token = current_user.generate_auth_token(600000)
            print token
            current_user.setToken(token)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
