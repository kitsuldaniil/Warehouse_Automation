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


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        session_clear()
        login = request.form['login']
        passw = request.form['password']
        role = int(request.form['role'])  # /*was name slct*/
        # client_id = request.form['slct']

        if (User.query.filter_by(login=login).first() != None):
            return render_template('action.html',
                                   action='Пользователь с таким логином уже существует, попробуйте другой')
        user = User(login=login, password=passw, role=role)  # id=client_id
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('action.html', action='Ошибка подключения к базе данных, попробуйте позже')
        session['login'] = login
        session['role'] = role
        # session['client_id'] = client_id
        return redirect(url_for('dash'))
    if 'login' not in session:
        return render_template('reg.html')
    return redirect(url_for('dash'))


@app.route('/logout')
def logout():
    session_clear()
    return redirect(url_for('auth'))


def session_clear():
    session.pop('login', None)
    session.pop('role', None)
    session.pop('password', None)


@app.route('/table/<table>', methods=['GET'])
def show(table):
    if 'login' not in session:
        return render_template('login.html')
    tablename = table
    if tablename == "Товары на складе":
        table = db.session.query(Product, product_on_wh).filter(Product.id == product_on_wh.c.product_id).all()
        return render_template('show.html', table=table, tablename=tablename, role=session.get('role'))
    elif tablename == "Товары в накладной":
        cust_id = int(request.args['cust'])
        cust = Cust.query.filter_by(id=cust_id).first()
        table = db.session.query(Product, product_in_cust).filter(Product.id == product_in_cust.c.product_id) \
            .filter(product_in_cust.c.cust_id == cust_id).all()
        return render_template('show.html', table=table, tablename=tablename, role=session.get('role'), cust_id=cust_id,ctype=cust.type)
    elif tablename == "Приход":
        table = Cust.query.filter(Cust.type == 1).all()
        return render_template('show.html', table=table, tablename=tablename, role=session.get('role'))
    elif tablename == "Реализация":
        table = Cust.query.filter(Cust.type == 2).all()
        return render_template('show.html', table=table, tablename=tablename, role=session.get('role'))
    table = tables[table]
    return render_template('show.html', table=table.query.all(), tablename=tablename, role=session.get('role'))


@app.route('/add/user', methods=['POST', 'GET'])
def add_user():
    if 'login' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        login = request.form["login"]
        password = request.form['password']
        role = request.form['role']
        user = User(login, password, int(role))
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('action.html', action='Ошибка подключения к базе данных, попробуйте позже')
        return render_template('action.html', action='Пользователь "' + login + '" был упешно добавлен')

    return render_template('adduser.html')
@app.route('/add/product', methods=['POST', 'GET'])
def add_product():
    if 'login' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form["name"]
        product = Product(name=name)
        try:
            db.session.add(product)
            db.session.commit()
        except:
            return render_template('action.html', action='Ошибка подключения к базе данных, попробуйте позже')
        return render_template('action.html', action='Товар "' + name + '" был упешно добавлен')

    return render_template('addproduct.html')


@app.route('/add/contractor', methods=['POST', 'GET'])
def add_contractor():
    if 'login' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form["name"]
        role = request.form['role']
        contractor = Contractor(name, int(role))
        try:
            db.session.add(contractor)
            db.session.commit()
        except:
            return render_template('action.html', action='Ошибка подключения к базе данных, попробуйте позже')
        return render_template('action.html', action='Контрагент "' + name + '" был упешно добавлен')

    return render_template('addcontractor.html')
	
@app.route('/add/contractor', methods=['POST', 'GET'])
def add_contractor():
    if 'login' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form["name"]
        role = request.form['role']
        contractor = Contractor(name, int(role))
        try:
            db.session.add(contractor)
            db.session.commit()
        except:
            return render_template('action.html', action='Ошибка подключения к базе данных, попробуйте позже')
        return render_template('action.html', action='Контрагент "' + name + '" был упешно добавлен')

    return render_template('addcontractor.html')


@app.route('/edit/<table>', methods=['POST', 'GET'])
def edit(table):
    if 'login' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        if table == 'Пользователи':
            try:
                user = User.query.filter_by(id=int(request.form['idedit'])).first()
                user.login = request.form['login']
                user.password = request.form['password']
                user.role = int(request.form['role'])
                db.session.commit()
            except:
                return render_template('action.html', action="Не удалось найти указанного пользователя")
            return render_template('action.html', action="Пользователь был успешно изменён")

        if table == 'Товары':
            try:
                product = Product.query.filter_by(id=int(request.form['idedit'])).first()
                product.name = request.form['name']
                db.session.commit()
            #     Возможно сделать предупреждение, что все записи товаров в накладных и на складе изменятся
            except:
                return render_template('action.html', action="Не удалось найти указаный товар")
            return render_template('action.html', action="Товар был успешно изменён")
        if table == 'Контрагенты':
            try:
                contractor = Contractor.query.filter_by(id=int(request.form['idedit'])).first()
                contractor.name = request.form['name']
                contractor.role = int(request.form['role'])
                db.session.commit()
            #     Возможно сделать предупреждение тоже
            except:
                return render_template('action.html', action="Не удалось найти контрагента")
            return render_template('action.html', action="Контрагент был успешно изменён")

    if request.method == 'GET':
        obj = tables[table]
        id = int(request.args.get('idedit'))
        try:
            item = obj.query.filter_by(id=id).first()
            if item != None:
                return render_template('edit.html', table=table, item=item)
            return render_template('action.html', action='Запись не найдена')
        except:
            return render_template('action.html',
                                   action='Ошибка: соединение с базой данных не установлено. Попробуйте позже')


@app.route('/delete/<table>', methods=['GET'])
def delete(table):
    if 'login' not in session:
        return render_template('login.html')
    name = str(table).lower()[:-1]
    try:
        obj = tables[table]
        item = obj.query.filter_by(id=int(request.args.get('iddel'))).first()
        db.session.delete(item)
        db.session.commit()
    except:
        return render_template('action.html', action="Запись не найдена. Возможно " + name + " уже удалён")

    return render_template('action.html', action=name + ' успешно удалён')


@app.route('/add/cust', methods=['POST', 'GET'])
def add_cust():
    if request.method == 'GET':
        # many queries
        return render_template('addcust.html', wh=Warehouse.query.all(), contractors=Contractor.query.all())
    if request.method == 'POST':
        name = request.form['name']
        date = datetime.datetime.strptime(str(request.form['date']), '%Y-%m-%d')
        # date = request.form['date']
        wh_id = int(request.form['wh'])
        c_id = int(request.form['contractor'])
        typ = int(request.form['type'])
        new_date = str(date.day) +'-'+ str(date.month) +'-'+ str(date.year)

        if typ==1:
            products = Product.query.all()
        else:
            products = db.session.query(Product, product_on_wh).filter(Product.id == product_on_wh.c.product_id).all()
        try:
            cust = None
            cust = Cust(name=name, date=new_date, c_id=c_id, wh_id=wh_id, type=typ)
            db.session.add(cust)
            db.session.commit()
        # table = db.session.query(Product, product_on_wh).filter(Product.id == product_on_wh.c.product_id).all()
        # Cust is empty, so table here is not required
        except Exception as e:
            return render_template('action.html', action="Сбой создания накладной. Попробуйте позже.")

        return render_template('pr_to_cust.html', tablename=name, c_id=cust.id, custtype=typ, table=[], products=products)
		
@app.route('/add/pr_to_cust', methods=['POST', 'GET'])
def pr_to_cust():
    if request.method == 'POST':
        c_id = int(request.form['c_id'])
        product_id = int(request.form['product_id'])
        count = int(request.form['count'])
        price = float(request.form['price'])
        cust = Cust.query.filter_by(id=c_id).first()

        if cust.type == 2:
            pr_on_wh = db.session.query(product_on_wh).filter_by(product_id=product_id).first()
            if pr_on_wh.count < count:
                return render_template('action.html', action='Недостаточно товара на складе')
            products = db.session.query(Product, product_on_wh).filter(Product.id == product_on_wh.c.product_id).all()
        else:
            products = Product.query.all()
        ins = product_in_cust.insert().values(cust_id=c_id, product_id=product_id, count=count, price=price)
        conn = engine.connect()
        conn.execute(ins)

        cust = Cust.query.filter_by(id=c_id).first()
        table = db.session.query(Product, product_in_cust).filter(Product.id == product_in_cust.c.product_id) \
            .filter(product_in_cust.c.cust_id == c_id).all()
        return render_template('pr_to_cust.html', tablename=cust.name, c_id=cust.id, custtype=cust.type, table=table, products=products)
    return render_template('addcust.html')

'''
stmt = users.update().\
            where(users.c.id==5).\
            values(name='user #5')          
            db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)
'''


@app.route('/execute', methods=['GET'])
def execute():
    # if request.method == 'POST':
    cust_id = int(request.args['cust_id'])
    cust = Cust.query.filter_by(id=cust_id).first()
    # result = db.session.query(product_on_wh).all()
    # print(str(result))
    query = db.session.query(product_in_cust).filter(product_in_cust.c.cust_id == cust_id).all()
    if cust.type == 1:
        for q in query:
            item = db.session.query(product_on_wh).filter_by(product_id=q.product_id).first() # distinct
            if item != None:
                new_count = item.count + q.count

                up = product_on_wh.update().where(product_on_wh.c.product_id == item.product_id).\
                                                values(count=new_count)
                conn = engine.connect()
                conn.execute(up)
            else:
                ins = product_on_wh.insert().values(wh_id=1, product_id=q.product_id, count=q.count, price=q.price)
                conn = engine.connect()
                conn.execute(ins)
                # product_on_wh.insert(1, q.product_id, q.count, q.price)
                # db.session.commit()
    if cust.type == 2:
        for q in query:
            item = db.session.query(product_on_wh).filter_by(product_id=q.product_id).first()  # find product on wh by product_id in cust
            if item != None:    # q - объект товара в накладной   item - товар на складе
                if item.count < q.count:
                    db.session.rollback()
                    product = Product.query.filter_by(id=item.product_id).first()
                    return render_template('action.html', action='Недостаточное количество товара "'
                                                                 + product.name + '" на складе')
                elif item.count == q.count:
                    deletion = product_on_wh.delete().where(product_on_wh.c.product_id == item.product_id)
                    conn = engine.connect()
                    conn.execute(deletion)
                else:
                    new_count = item.count - q.count
                    up = product_on_wh.update().where(product_on_wh.c.product_id == item.product_id). \
                        values(count=new_count)
                    conn = engine.connect()
                    conn.execute(up)
    cust = None
    try:
        # cust = Cust.query.filter_by(id=cust_id).first()
        # db.session.delete(cust)
        # db.session.commit()
        del_cust(cust_id)
    except:
        return render_template('action.html', action='Накладная не удалена')
    return render_template('action.html', action='Накладная проведена успешно')
@app.route('/delete/cust', methods=['GET'])
def delete_cust():
    if 'login' not in session:
        return render_template('login.html')
    # try:
        # obj = tables[table]
    item = Cust.query.filter_by(id=int(request.args.get('iddel'))).first()
    db.session.delete(item)
    db.session.commit()
    # except:
    #     return render_template('action.html', action="Запись не найдена. Возможно накладная уже удалена")

    return render_template('action.html', action='Накладная успешно удалена')



def del_cust(id):
    cust = Cust.query.filter(Cust.id == id).first()
    db.session.delete(cust)
    db.session.commit()

def get_product_name(product_id):
    query = Product.query.get(product_id).first()
    return query.name


if __name__ == '__main__':
    app.run(debug=True)

"""
"""
