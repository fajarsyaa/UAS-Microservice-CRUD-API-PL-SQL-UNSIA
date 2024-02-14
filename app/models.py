from datetime import datetime 
from app import db

class Customer(db.Model):
    __tablename__ = 'ms_customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255),nullable=False)
    no_rek = db.Column(db.Integer,  unique=True, nullable=False)

    def __repr__(self):
        return '<Customer %r>' % self.username

class Merchant(db.Model):
    __tablename__ = 'ms_merchant'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255),nullable=False)
    no_rek = db.Column(db.Integer,  unique=True, nullable=False)

    def __repr__(self):
        return '<Merchant %r>' % self.username

class Transaction(db.Model):
    __tablename__ = 'trx_payment'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('ms_customer.id'), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('ms_merchant.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref='payments')
    merchant = db.relationship('Merchant', backref='payments')

    def __repr__(self):
        return '<Transaction %r>' % self.id