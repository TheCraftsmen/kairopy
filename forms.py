# -*- coding: utf-8 -*-
"""Forms for the bull application."""
from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired
from app import db

class LoginForm(Form):
    """Form class for user login."""
    username = TextField('USUARIO', validators=[DataRequired()])
    password = PasswordField('CONTRASEÑA', validators=[DataRequired()])


class LogupForm(Form):
    """Form class for user logup."""
    username = TextField('USUARIO', validators=[DataRequired()])
    email = TextField('EMAIL', validators=[DataRequired()])
    password = PasswordField(u'CONTRASEÑA', validators=[DataRequired()])
    repeatpassword = PasswordField(u'REPETIR CONTRASEÑA', validators=[DataRequired()])

class ResetForm(Form):
    """Form class for user logup."""
    username = TextField('USUARIO', validators=[DataRequired()])