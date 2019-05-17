from flask import Flask, request, json, jsonify, make_response, abort, session, render_template, redirect, url_for
from application.app import app, db
from application.classes import *
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import insert, update, delete, create_engine, text
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'wh.db')
engine = create_engine(db_uri)

tables = {'Пользователи': User,
          'Товары': Product,
          'Контрагенты': Contractor,
          'Склады': Warehouse,
          'Накладные': Cust
          }


@app.route('/', methods=['POST', 'GET'])  #
def dash():
    if 'login' not in session:
        return redirect(url_for('auth'))
    return render_template('main.html', role=session.get('role'))


# client=classes.Client.query.filter_by(id=session.get('client_id')).first().name)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        session_clear()
        login = request.form['login']
        passw = request.form['password']
        auth = User.query.filter_by(login=login, password=passw).first()
        if (auth != None):
            session['login'] = auth.login
            session['role'] = auth.role  # 1 - admin, 2-manager, 3-wh worker
            # session['client_id'] = auth.client_id
            return redirect(url_for('dash'))
        else:
            return render_template('action.html',
                                   action='Не удалось авторизоваться, проверьте правильность введенных данных')
    if 'login' not in session:
        return render_template('login.html')
    return redirect(url_for('dash'))


