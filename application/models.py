from datetime import date
from application.database import db



class User(db.Model):
    __tablename__ = "sneakers_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    guest = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String, nullable=False, default="Admin No Address")
    postal_code = db.Column(db.Integer, nullable=False, default="Admin No Zipcode")
    contact_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    store_name =db.Column(db.Integer, nullable=False, default="User No Store")



class Product(db.Model):
    __tablename__ = "sneakers_products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    category_name=db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    discount = db.Column(db.Integer, nullable=False, default=0)   
    price = db.Column(db.Float, nullable=False)
    size_36 = db.Column(db.Integer, nullable=False)
    size_37 = db.Column(db.Integer, nullable=False)
    size_38 = db.Column(db.Integer, nullable=False)
    size_39 = db.Column(db.Integer, nullable=False)
    size_40 = db.Column(db.Integer, nullable=False)
    size_41 = db.Column(db.Integer, nullable=False)
    size_42 = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    date_added = db.Column(db.String, nullable=False,default=date.today)


class Review(db.Model):
    __tablename__ = "sneaker_review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, unique=False, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    prod_id = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    __tablename__ = "sneakers_cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Integer, nullable=False,default=date.today)

class WishList(db.Model):
    __tablename__ = "sneakers_wishlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Integer, nullable=False,default=date.today)
  

class Purchase(db.Model):
    __tablename__ = "purchases_sneakers_stores_n"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.Integer, nullable=False)
    customer_user = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
    order_id = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = "sneaker_orders_n"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_price =db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String, nullable=False, default="In Process")
    returned = db.Column(db.String, nullable=False, default="No")
    cancelled = db.Column(db.String, nullable=False, default="No")

class Payments(db.Model):
    __tablename__ = "aerostride_trans"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    payment_id = db.Column(db.Integer, nullable=False)
    total_price =db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
    refund = db.Column(db.String, nullable=False, default="no")

class Issue(db.Model):
    __tablename__ = "sneaker_issues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)

