"""
Initialize Flask extensions.

This module initializes the Flask extensions
used in the application, including SQLAlchemy
for database management, Flask-Migrate for handling database
migrations, Flask-Login for user authentication management,
and Flask-Admin for administrative interfaces.

The initialized extensions are:
    - db (SQLAlchemy):
        SQLAlchemy instance for database management.
    - migrate (Migrate):
        Flask-Migrate instance for handling database migrations.
    - login_manager (LoginManager):
        Flask-Login instance for user authentication management.
    - admin (Admin):
        Flask-Admin instance for administrative interfaces.
"""
# from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# migrate = Migrate()
login_manager = LoginManager()
db = SQLAlchemy()

def init_db(app):
    '''
    Initializes the database
    '''
    db.init_app(app=app)

    # Create the database tables
    with app.app_context():
        db.create_all()

def init_login_manager(app):
    '''
    Initializes the login manager
    '''
    login_manager.init_app(app=app)
