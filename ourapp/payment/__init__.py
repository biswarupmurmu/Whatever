from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ourapp import db
from ourapp.models import CartItem, Product

payment_bp=Blueprint("payment",__name__,template_folder="templates",url_prefix="/payment")

@payment_bp.route('/')
@login_required
def payment():
    return render_template("payment/payment.html")