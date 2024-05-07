"""
User view module
"""

from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ourapp.models import CartItem, Product
from ourapp.logging_config.config import logger
from ourapp.extensions import db

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/")


@user_bp.route("/profile")
@login_required
def view_profile():
    """
    Render the user's profile page.

    Returns:
        str: Rendered HTML template for the user's profile page.
    """
    logger.info("Viewing %s(%s) user profile.", current_user.fname, current_user.id)
    return render_template("user/profile.html")


@user_bp.route("/update-address", methods=["POST"])
@login_required
def update_address():
    """
    Update the user's address.

    Returns:
        redirect: Redirect to view the user's cart page.
    """
    current_user.address = request.form["newAddress"]
    db.session.commit()
    flash(message="Addredd updated successfully", category="success")
    logger.info(
        "Customer %s(%s) Address updated successfully.",
        current_user.fname,
        current_user.id,
    )
    return redirect(url_for("cart.view_cart"))


@user_bp.route("/update-password", methods=["POST"])
@login_required
def update_password():
    """
    Update the user's password.

    Returns:
        redirect: Redirect to view the user's profile page.
    """
    if request.method == "POST":
        old_password = request.form["oldPassword"]
        new_password = request.form["newPassword"]
        confirm_password = request.form["confirmPassword"]
        if not check_password_hash(current_user.password, old_password):
            flash("Invalid old password. Please try again.", "error")
            logger.warning(
                "Invalid old password provided by Customer %s(%s) during password update.",
                current_user.fname,
                current_user.id,
            )
            return redirect(url_for("user.view_profile"))

        if new_password != confirm_password:
            flash(
                "New password and confirm password do not match. Please try again.",
                "error",
            )
            logger.warning(
                "New password and confirm password provided by Customer %s(%s) do not match.",
                current_user.fname,
                current_user.id,
            )
            return redirect(url_for("user.view_profile"))

        if check_password_hash(current_user.password, new_password):
            flash("New Password and Old Password Cannote be same", "info")
            logger.warning(
                "New password and old password provide by Customer %s(%s) are the same.",
                current_user.fname,
                current_user.id,
            )
            return redirect(url_for("user.view_profile"))

        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Password updated successfully.", "success")
        logger.info(
            "Password for Customer %s(%s) is updated successfully.",
            current_user.fname,
            current_user.id,
        )
        return redirect(url_for("user.view_profile"))

    return redirect(url_for("user.view_profile"))
