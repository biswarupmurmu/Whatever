from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import current_user, login_required
from ourapp import db
from ourapp.models import CartItem, Product
from werkzeug.security import generate_password_hash, check_password_hash

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

@user_bp.route("/update-password", methods=['POST'])
@login_required
def update_password():
    if request.method == 'POST':
        old_password = request.form['oldPassword']
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']
        if not check_password_hash(current_user.password,old_password):
            flash('Invalid old password. Please try again.', 'error')
            return redirect(url_for('user.view_profile'))

        if new_password != confirm_password:
            flash('New password and confirm password do not match. Please try again.', 'error')
            return redirect(url_for('user.view_profile'))
        
        if check_password_hash(current_user.password,new_password):
            flash('New Password and Old Password Cannote be same', 'info')
            return redirect(url_for('user.view_profile'))

        current_user.password=generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('user.view_profile'))

    return redirect(url_for('user.view_profile'))  

