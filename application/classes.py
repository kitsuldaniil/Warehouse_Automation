from app import db

'''
add password hashing and new columns and functions for checking
'''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Integer, default=1)

    def __init__(self, login, password, role):
        self.login = login
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.login


product_on_wh = db.Table('product_on_wh', db.Column('wh_id', db.Integer, db.ForeignKey('warehouse.id')),
                                          db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                                          db.Column('count', db.Integer), db.Column('price', db.Float))


class Warehouse(db.Model):
    __tablename__ = 'warehouse'
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
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # price = db.Column(db.Float)

    def __init__(self, name):
        self.name = name
        # self.price = price

    def __repr__(self):
        return '<Product %r>' % self.name


product_in_cust = db.Table('product_in_cust', db.Column('cust_id', db.Integer, db.ForeignKey('cust.id', ondelete='CASCADE')),
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                           db.Column('count', db.Integer), db.Column('price', db.Float))


class Contractor(db.Model):
    __tablename__ = 'contractor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.Integer)

    custs = db.relationship('Cust', backref='contractor')

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __repr__(self):
        return '<Contractor %r>' % self.name


class Cust(db.Model):
    __tablename__ = 'cust'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.String(50))
    type = db.Column(db.Integer, nullable=False)

    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    wh_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)

    products = db.relationship('Product', secondary=product_in_cust,
                               backref=db.backref('cust', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, name, date, c_id, wh_id, type):
        self.name = name
        self.date = date
        self.contractor_id = c_id
        self.wh_id = wh_id
        self.type = type

    def __repr__(self):
        return '<Cust %r>' % self.name


'''
Внедрить:
подумать про автоинкремент
'''
