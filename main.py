
from flask import Flask as f
from application.database import db
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from application.models import User, Store_Category, Product, Purchase, Order
import stripe

def create_app():
    app = f(__name__,template_folder='template',static_url_path='/static',static_folder='static')
    stripe.api_key = 'sk_test_51NhU8KSD25c7XMJIL1FGpIKixd5X2EP11u7zVUxY69wOY8O3p2uuynkoVC23ZwSsXuEtUbLveFjGAAGFPpncJRKd00U3ssaK6G'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "abcd234"

    db.init_app(app)

    app.app_context().push()

    return app

app = create_app()
migrate = Migrate(app, db)
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Store_Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Purchase, db.session))
admin.add_view(ModelView(Order, db.session))

from application.controllers import *

if __name__=="__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=2080, debug=True)