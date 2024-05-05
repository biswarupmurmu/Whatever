from datetime import datetime
from . import db
from flask_login import UserMixin

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    verified_email = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.Text(150))
    
    # New lines added
    cart = db.relationship('CartItem', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    # End of new lines

    def __repr__(self):
        return f'{self.id} {self.fname} {self.lname}'

product_category = db.Table(
    "product_category",
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    small_description = db.Column(db.String(100), nullable=False)
    image_url=db.Column(db.String(150), nullable=False)
    features=db.Column(db.Text, nullable=False)
    categories = db.relationship('Category', secondary=product_category, backref=db.backref('products', lazy='dynamic'))

    def __repr__(self):
        return f'{self.id} {self.name}'
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.name}'


# New lines
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # customer = db.relationship('Customer', backref='orders')
    ordered_date=db.Column(db.DateTime, default=datetime.now())
    arriving_date=db.Column(db.DateTime)
    status=db.Column(db.String(100),nullable=False,default='confirmed')
    date_according_to_status=db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.Text(150))
    ordered_items = db.relationship('OrderedItem', backref='order', cascade='all, delete-orphan')
    feedback = db.Column(db.Text(300))
    
    def __repr__(self):
        return f'{self.id} ordered on {self.ordered_date}'
    
#
class OrderedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='ordered_items')
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(100), nullable=False)



