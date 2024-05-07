"""
Models defined here
"""

from datetime import datetime

from flask_login import UserMixin

from ourapp.extensions import db


class Customer(UserMixin, db.Model):
    """
    Model representing a customer.

    Attributes:
        id (int): The unique identifier for the customer.
        fname (str): The first name of the customer.
        lname (str): The last name of the customer.
        email (str): The email address of the customer (unique).
        password (str): The password of the customer.
        verified_email (bool): Flag indicating if the email address is verified.
        address (str): The address of the customer.
        cart (relationship): Relationship to CartItem model, representing items
        in the customer's cart.
        orders (relationship): Relationship to Order model, representing orders
        made by the customer.
    """

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    verified_email = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.Text(150))

    # New lines added
    cart = db.relationship("CartItem", backref="customer", lazy=True)
    orders = db.relationship("Order", backref="customer", lazy=True)
    # End of new lines

    def __repr__(self):
        return f"{self.id} {self.fname} {self.lname}"

    def is_admin(self):
        """
        returns true if admin
        """
        return False


product_category = db.Table(
    "product_category",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column(
        "category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True
    ),
)


# pylint: disable=too-few-public-methods
class Product(db.Model):
    """
    Model representing a product.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
        description (str): The description of the product.
        small_description (str): A brief description of the product.
        image_url (str): The URL of the product's image.
        features (str): Features of the product.
        categories (relationship):
        Relationship to Category model, representing categories
         the product belongs to.
        cart_items (relationship): Relationship to CartItem model,
         representing cart items associated with the product.
        ordered_items (relationship): Relationship to OrderedItem model,
        representing ordered items associated with the product.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    small_description = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(150), nullable=False)
    features = db.Column(db.Text, nullable=False)
    categories = db.relationship(
        "Category",
        secondary=product_category,
        backref=db.backref("products", lazy="dynamic"),
    )

    def __repr__(self):
        return f"{self.id} {self.name}"


# pylint: disable=too-few-public-methods
class Category(db.Model):
    """
    Model representing a category.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.name}"


# New lines
# pylint: disable=too-few-public-methods
class CartItem(db.Model):
    """
    Represents a cart item in the database.

    Attributes:
        id (int): The unique identifier for the cart item.
        quantity (int): The quantity of the product in the cart.
        customer_id (int): The foreign key referencing the customer associated with the cart item.
        product_id (int): The foreign key referencing the product associated with the cart item.
        product (relationship): Relationship with the Product object associated with the cart item.
    """

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product", backref="cart_items")


# pylint: disable=too-few-public-methods
class Order(db.Model):
    """
    Represents an order in the database.

    Attributes:
        id (int): The unique identifier for the order.
        customer_id (int): The foreign key referencing the customer who placed the order.
        ordered_date (datetime): The date and time when the order was placed.
        arriving_date (datetime): The expected arriving date of the order.
        status (str): The status of the order.
        date_according_to_status (datetime): The date and time when the status was updated.
        address (str): The address to which the order will be delivered.
        ordered_items (relationship): Relationship with OrderedItem objects
        associated with the order.
        feedback (str): The feedback provided for the order.
    """

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    # customer = db.relationship('Customer', backref='orders')
    ordered_date = db.Column(db.DateTime, default=datetime.now())
    arriving_date = db.Column(db.DateTime)
    status = db.Column(db.String(100), nullable=False, default="confirmed")
    date_according_to_status = db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.Text(150))
    ordered_items = db.relationship(
        "OrderedItem", backref="order", cascade="all, delete-orphan"
    )
    feedback = db.Column(db.Text(300))

    def __repr__(self):
        return f"{self.id} ordered on {self.ordered_date}"


#
# pylint: disable=too-few-public-methods
class OrderedItem(db.Model):
    """
    Represents an item within an order in the database.

    Attributes:
        id (int): The unique identifier for the ordered item.
        order_id (int): The foreign key referencing the order to which the item belongs.
        product_id (int): The foreign key referencing the product associated with the item.
        product (relationship): Relationship with the Product object associated with the item.
        quantity (int): The quantity of the product in the order.
        price (float): The price of the product in the order.
    """

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product", backref="ordered_items")
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(100), nullable=False)
