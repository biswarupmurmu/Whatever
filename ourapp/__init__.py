"""
This is the application factory for our application Whatever
"""

from flask import Flask, render_template
from flask_admin.contrib.sqla import ModelView

from .admin import admin

# from .models import Customer, Product, Category, Order, OrderedItem, CartItem
from .auth import auth
from .cart import cart_bp
from .extensions import init_db, init_login_manager
from .order import order_bp
from .payment import payment_bp
from .product import product_bp
from .public import public
from .user import user_bp


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    # app.config.from_envvar('OURAPPLICATION_SETTINGS')
    ######################################################
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SECRET_KEY"] = "Super secret key"
    ######################################################

    init_db(app=app)
    init_login_manager(app=app)
    admin.init_app(app=app)

    @app.errorhandler(404)
    def not_found(e):
        """
        custom 404 error handler
        """
        return render_template("error_404.html", e=e)

    app.register_blueprint(auth)
    app.register_blueprint(public)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)

    # Add views for each model
    # I dont know how it works, but it works
    # Category()
    # admin.add_view(ModelView(Customer, db.session))
    # admin.add_view(ModelView(Product, db.session))
    # admin.add_view(ModelView(Category, db.session))
    # admin.add_view(ModelView(Order, db.session))
    # admin.add_view(ModelView(OrderedItem, db.session))
    # admin.add_view(ModelView(CartItem, db.session))

    return app
