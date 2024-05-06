'''
This module handles the user authentication for our application.
'''
from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from ourapp.models import Customer
from ourapp import db
from ourapp import login_manager
from .form import LoginForm, SignupForm
from random import randint

auth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        form.process_data()
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = Customer.query.filter_by(email=email).first()
            if not user:
                form.email.errors = ["Email not registered."]
            elif not check_password_hash(user.password, password):
                form.password.errors = ["Wrong password entered."]
            elif user and check_password_hash(user.password, password):
                login_user(user)
                requested_next_route = request.args.get('next')
                flash("Login successful", category="success")
                return redirect(requested_next_route or url_for('public.index'))
    return render_template('auth/login.html', form=form)


def generate_customer_id():
    return randint(10**6,(10**7)-1)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    '''
    This is the signup method
    '''
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
            else:
                while True:
                    customer_id = generate_customer_id()
                    if not Customer.query.filter_by(id=customer_id).first():
                        break

                user = Customer(
                    id = customer_id,
                    fname=fname,
                    lname=lname,
                    email=email,
                    password=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
                flash(message=f"{user.fname} {user.id}", category="user_registered_success")
                return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    '''
    This handles the logout funtionality
    '''
    logout_user()
    flash('Logout Successful!','success')
    return redirect(url_for("public.index"))


# Login Manager setup
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    '''
    Loads the user as per the instructions in Flask-Login module
    '''
    return Customer.query.get(int(user_id))
