"""
This Module validates payment credentials.
"""

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, ValidationError, length


def numbers_only(form, field):
    if not str(field.data).isdigit():
        raise ValidationError('Only numbers allowed')
    return True

def validate_expiry(form, field):
    if not str(field.data).isdigit():
        raise ValidationError("Invalid input")
    m = field.data[:2]
    y = field.data[2:6]
    if datetime.now() > datetime(int(y), int(m), 1):
        raise ValidationError("Card expired")

class PaymentForm(FlaskForm):
    card_no = StringField(
        "Card no", validators=[InputRequired(), length(min=16, max=16), numbers_only]
    )
    name = StringField("Card holders name", validators=[InputRequired()])
    expiry_date = StringField("Expiry" , validators=[InputRequired(), length(min=6,max=6), validate_expiry])
    cvv = StringField("CVV", validators=[InputRequired(), length(min=3, max=3), numbers_only])

