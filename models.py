from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable = False)
    passhash = db.Column(db.String(256), nullable = False)
    name = db.Column(db.String(64), nullable = True)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)

    ## relationships
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    man_date = db.Column(db.Date, nullable = False)
    
    ## relationships
    carts = db.relationship('Cart', backref='product', lazy=True)
    orders = db.relationship('Order', backref='product', lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    total = db.Column(db.Float, nullable = False)
    
    ## relationships
    orders = db.relationship('Order', backref='transaction', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)

# create database if it doesn't exist
with app.app_context():
    db.create_all()