"""
Admin functionality
"""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required

from ourapp.extensions import db
from ourapp.models import Customer  # Import your SQLAlchemy models


class SeccureModelView(ModelView):
    '''
    Restrict user(except admin)
    '''
    @login_required
    def is_admin(self):
        '''
        Check if the user is admin
        '''
        return current_user.is_authenticated and current_user.is_admin()


admin = Admin()
admin.add_view(SeccureModelView(Customer, db.session))
