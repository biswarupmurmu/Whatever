'''
This module handles the user authentication for our application.
'''
from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from ourapp.models import Customer
from ourapp import db
from ourapp import login_manager
from .form import SignupForm

auth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Customer.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            requested_next_route = request.args.get('next')
            return redirect(requested_next_route or url_for('public.index'))
        else:
            flash('Wrong email or password. Please try again.', 'error')  # Flash message for wrong credentials
            return redirect(url_for('auth.login'))  # Redirect back to the login page
    return render_template('auth/login.html')




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
                user = Customer(
                    fname=fname,
                    lname=lname,
                    email=email,
                    password=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    '''
    This handles the logout funtionality
    '''
    logout_user()
    return redirect(url_for("public.index"))


# Login Manager setup
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    '''
    Loads the user as per the instructions in Flask-Login module
    '''
    return Customer.query.get(int(user_id))
