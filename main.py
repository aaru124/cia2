
from flask import Flask as f
import razorpay
from application.database import db
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from application.models import User, Product, Purchase, Order, Review, Cart, WishList
import stripe

def create_app():
    app = f(__name__,template_folder='template',static_url_path='/static',static_folder='static')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "abcd234"

    razorpay_client = razorpay.Client(auth=("rzp_test_XOy0arNBRKuF4z", "eGVaXmXbQbQWygImcrjIaQ8i"))

    db.init_app(app)

    app.app_context().push()

    return app

app = create_app()
migrate = Migrate(app, db)
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Purchase, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Cart, db.session))
admin.add_view(ModelView(WishList, db.session))

from application.controllers import *

if __name__=="__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=2080, debug=True)