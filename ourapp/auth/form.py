"""
This module validates Signup and Login forms for customers.

This module provides FlaskForm classes for validating and processing Signup
and Login forms submitted by customers.
"""
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, length


class SignupForm(FlaskForm):
    '''
    Create a Signup Form for customers.

    Inherits:
        FlaskForm: Base class for creating forms in Flask.

    Attributes:
        fname (StringField): Field for entering first name.
        lname (StringField): Field for entering last name.
        email (EmailField): Field for entering email address.
        password (PasswordField): Field for entering password.
        confirm_password (PasswordField): Field for confirming password.

    '''
    fname = StringField("First name", validators=[InputRequired()])
    lname = StringField("Last name")
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            length(min=4, max=20),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def process_data(self):
        '''
        Process form data by stripping leading and trailing spaces from fields.
        '''
        self.fname.data = self.fname.data.strip()
        self.lname.data = self.lname.data.strip()
        self.email.data = self.email.data.strip().lower()


class LoginForm(FlaskForm):
    '''
    Create a Login Form for customers.

    Inherits:
        FlaskForm: Base class for creating forms in Flask.

    Attributes:
        email (EmailField): Field for entering email address.
        password (PasswordField): Field for entering password.

    '''
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


    def process_data(self):
        '''
        Process form data by converting email to lowercase and stripping leading and trailing spaces.
        '''
        self.email.data = self.email.data.strip().lower()
