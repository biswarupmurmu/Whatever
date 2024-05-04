from flask import Flask
from .extensions import db, migrate, login_manager, admin
from .models import Customer, Product, Category, Order, OrderedItem, CartItem
from flask_admin.contrib.sqla import ModelView

def create_app():
    app = Flask(__name__)
    # app.config.from_envvar('OURAPPLICATION_SETTINGS')
    ######################################################
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SECRET_KEY'] = "Super secret key"
    ######################################################

    from .auth import auth
    from .public import public
    from .user import user_bp
    from .product import product_bp
    from .cart import cart_bp
    from .order import order_bp
    from .payment import payment_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(public)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)

    # Initialize Flask extensions here
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    admin.init_app(app=app)


    # Create the database tables
    with app.app_context():
        db.create_all()
    

    # Add views for each model
    # I dont know how it works, but it works
    Category()
    admin.add_view(ModelView(Customer, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(OrderedItem, db.session))
    admin.add_view(ModelView(CartItem, db.session))
    return app
