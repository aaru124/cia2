from datetime import date
from application.database import db



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

class Store_Category(db.Model):
    __tablename__="store_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Product(db.Model):
    __tablename__ = "store_product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    category_name=db.Column(db.String, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    manufacturing_date = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)

class Purchase(db.Model):
    __tablename__ = "purchases_stores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.Integer, nullable=False)
    owner_store = db.Column(db.Integer, nullable=False)
    customer_user = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price =db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
