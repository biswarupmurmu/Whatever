"""
This module provides functionality for validating payment credentials and includes a PaymentForm class.

Functions:
    numbers_only: Validates that the input contains only numbers.
    alphabets_only: Validates that the input contains only alphabets.
    validate_expiry: Validates the expiry date format and checks if the card is expired.

Classes:
    PaymentForm: Inherits from FlaskForm and provides fields for card number, cardholder's name,
        expiry date, and CVV with corresponding validators.
"""

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, ValidationError, length


def numbers_only(form, field):
    """
    Validate that the input contains only numbers.

    Args:
        form (FlaskForm): The form object.
        field (str): The field to validate.

    Raises:
        ValidationError: If the input contains non-numeric characters.
    """
    if not str(field.data).isdigit():
        raise ValidationError('Only numbers allowed')
    return True

def alphabets_only(form, field):
    """
    Validate that the input contains only alphabets.

    Args:
        form (FlaskForm): The form object.
        field (str): The field to validate.

    Raises:
        ValidationError: If the input contains non-alphabetic characters.
    """
    if not str(field.data).isalpha():
        raise ValidationError('Only alphabets allowed')
    return True

def validate_expiry(form, field):
    """
    Validate the expiry date format and check if the card is expired.

    Args:
        form (FlaskForm): The form object.
        field (str): The expiry date field to validate.

    Raises:
        ValidationError: If the expiry date is not in MMYYYY format or if the card is expired.
    """
    if not str(field.data).isdigit():
        raise ValidationError("Invalid input")
    m = int(field.data[:2])
    y = int(field.data[2:6])

    if m > 12 or m <=0:
        raise ValidationError("Invalid month")

    if datetime.now() > datetime(y, m, 1):
        raise ValidationError("Card expired")

class PaymentForm(FlaskForm):
    """
    A form for validating payment credentials.

    Attributes:
        card_no (StringField): Field for the card number with validators for length and numeric input.
        name (StringField): Field for the cardholder's name with validators for alphabetic input.
        expiry_date (StringField): Field for the expiry date in MMYYYY format with validators for length,
            format, and expiry check.
        cvv (StringField): Field for the CVV with validators for length and numeric input.
    """
    card_no = StringField(
        "Card no", validators=[InputRequired(), length(min=16, max=16), numbers_only]
    )
    name = StringField("Card holders name", validators=[InputRequired(), alphabets_only])
    expiry_date = StringField("Expiry(MMYYYY)" , validators=[InputRequired(), length(min=6,max=6), validate_expiry])
    cvv = StringField("CVV", validators=[InputRequired(), length(min=3, max=3), numbers_only])

