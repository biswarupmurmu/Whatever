from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from ourapp import db
from ourapp.models import CartItem, Product

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/")

@user_bp.route("/profile")
@login_required
def view_profile():
    return render_template("user/profile.html")

@user_bp.route("/update-address", methods=['POST'])
@login_required
def update_address():
    current_user.address = request.form['newAddress']
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

