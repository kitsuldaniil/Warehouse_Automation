from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    privelegy = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.login


product_on_wh = db.Table('product_on_wh', db.Column('wh_id', db.Integer, db.ForeignKey('warehouse.id')),
                         db.Column('pr_id', db.Integer, db.ForeignKey('product.id')), db.Column('count'), db.Integer)


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))

    products = db.relationship('Product', secondary=product_on_wh,
                               backref=db.backref('warehouse', lazy='dynamic'),
                               lazy='dynamic')
    custs = db.relationship('Cust', backref='warehouse')

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return '<Warehouse %r>' % self.name


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Product %r>' % self.name


class Cust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

    contragent_id = db.Column(db.Integer, db.ForeignKey('contragent.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)

    products = db.relationship('Product', secondary=product_in_cust,
                               backref=db.backref('cust', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, date, c_id, w_id):
        self.date = date
        self.contragent_id = c_id
        self.warehouse_id = w_id

    def __repr__(self):
        return '<Cust %r>' % self.name


product_in_cust = db.Table('prod_on_cust', db.Column('cust_id'), db.Integer, db.ForeignKey('cust.id'),
                           db.Column('pr_id', db.Integer, db.ForeignKey('product.id')), db.Column('count'), db.Integer)


class Contragent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.String(50))

    custs = db.relationship('Cust', backref='contragent')

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __repr__(self):
        return '<Contragent %r>' % self.name


'''
Внедрить:
подумать про автоинкремент
'''
