"""
This module handles the user authentication for our application.

This module provides routes for user login, signup, and logout functionalities.
"""

from random import randint
from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from ourapp.extensions import db, login_manager
from ourapp.models import Customer
from ourapp.logging_config.config import logger
from .form import LoginForm, SignupForm


auth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    GET: Renders the login form.
    POST: Processes login form submission. If successful, logins the user and
    redirects to the requested page or the homepage.
    """
    form = LoginForm(request.form)
    if request.method == "POST":
        form.process_data()
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = Customer.query.filter_by(email=email).first()
            if not user:
                form.email.errors = ["Email not registered."]
                logger.warning("Attempted login with unregistered email: %s", email
                )
            elif not check_password_hash(user.password, password):
                form.password.errors = ["Wrong password entered."]
                logger.warning(
                    "Attempted login with incorrect password for email: %s", email
                )
            elif user and check_password_hash(user.password, password):
                login_user(user)
                requested_next_route = request.args.get("next")
                flash("Login successful", category="success")
                logger.info("User logged in successfully: %s", email)
                return redirect(requested_next_route or url_for("public.index"))
    return render_template("auth/login.html", form=form)


def generate_customer_id():
    """
    Generates random customer id
    """
    return randint(10**6, (10**7) - 1)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle user signup.

    GET: Renders the signup form.
    POST: Processes signup form submission. If successful, creates a new user
    account and redirects to the login page.
    """
    form = SignupForm(request.form)
    if request.method == "POST":
        form.process_data()
        if form.validate():
            fname = form.fname.data
            lname = form.lname.data
            email = form.email.data
            password = form.password.data

            email_exists = Customer.query.filter_by(email=email).first()
            if email_exists:
                form.email.errors = ["Email already in use."]
                logger.warning(
                    "Attempted signup with existing email: %s", 
                    email)
            else:
                while True:
                    customer_id = generate_customer_id()
                    if not Customer.query.filter_by(id=customer_id).first():
                        break

                user = Customer(
                    id=customer_id,
                    fname=fname,
                    lname=lname,
                    email=email,
                    password=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
                flash(
                    message=f"{user.fname} {user.id}",
                    category="user_registered_success",
                )
                logger.info("New account created: %s", email)
                return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """
    Handle user logout.

    Logs out the currently logged-in user and redirects to the homepage.
    """
    logout_user()
    flash("Logout Successful!", "success")
    logger.info("Logout Successful for Customer")
    return redirect(url_for("public.index"))


# Login Manager setup
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    """
    Load the user object from the database.

    This function is required by Flask-Login to load a user from the
    database based on the user_id provided.
    """
    return Customer.query.get(int(user_id))
