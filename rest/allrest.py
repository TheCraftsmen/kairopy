from flask import jsonify
from flask_restful import Resource
from models import *
from app import auth
import datetime
import sys

class AllTurn(Resource):


    @auth.login_required
    def get(self,user_id):
        if int(current_user.get_id()) != int(user_id): return
        listOfTurn = list()
        turnQuery = RequestList.query.filter(RequestList.status.in_((0, 1))).filter_by(user_id=user_id)
        if turnQuery:
            for row in turnQuery:
                dictOfTurn = dict(
                     table_id=row.table_id,
                     number=row.number,
                     status=row.status,
                     cust_name=row.cust_name,
                     user_id=row.user_id,
                     request_type=row.request_type
                    )
                listOfTurn.append(dictOfTurn)
        listOfSettings = list()
        us = UserSettings.query.filter_by(user_id=user_id).first()
        if us:
            dictOfSettings = { 'column_turn': us.column_turn ,
                           'column_custname': us.column_custname , 
                           'column_type': us.column_type }
            listOfSettings.append(dictOfSettings)
        return jsonify({'allTurn': listOfTurn, 'settings': listOfSettings})


class CleanAll(Resource):

    @auth.login_required
    def put(self,user_id):
        if int(current_user.get_id()) != int(user_id): return
        turnQuery = RequestList.query.filter_by(user_id=user_id)
        if turnQuery:
            for row in turnQuery:
                if row.status == 1: 
                    row.status += 1
                elif row.status == 0:
                    row.status += 2
        db.session.commit() 


class ChangeSettings(Resource):


    @auth.login_required
    def put(self, user_id, column_name, new_value):
        if int(current_user.get_id()) != int(user_id): return
        us = UserSettings.query.filter_by(user_id=user_id).first()
        if us:
            exec("us.%s = '%s' " % (column_name,new_value))
            #us[column_name] = new_value
            db.session.commit()
        return


class UpdateStatus(Resource):
    

    @auth.login_required
    def put(self, api_num, user):
        if int(current_user.get_id()) != int(user): return
        updateTurn = RequestList.query.filter_by(user_id=user).filter(RequestList.request_date >=datetime.date.today()).filter_by(number=api_num).limit(1)
        for row in updateTurn:
            row.status += 1
        db.session.commit()
        return {'api_num': api_num}
