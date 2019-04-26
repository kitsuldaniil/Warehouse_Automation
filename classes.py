from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    privelegy = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.login


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self):
        return '<Warehouse %r>' % self.name

class Cust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

    contragent_id = db.Column(db.Integer, db.ForeignKey('contragent.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)

    def __repr__(self):
        return '<Cust %r>' % self.name

class Conrtagent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)

class Cust_details(db.Model):
    count = db.Column(db.Integer)
