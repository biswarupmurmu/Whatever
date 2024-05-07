"""
Public view module
"""

from flask import Blueprint, render_template
from sqlalchemy import func

from ourapp.extensions import db
from ourapp.models import CartItem, Category, OrderedItem, Product

public = Blueprint("public", __name__, template_folder="templates", url_prefix="/")


def get_trending_products():
    """
    Get a list of trending products based on the number of occurrences in carts.

    Returns:
        List: A list of trending Product objects.
    """
    # Query to select Product objects and count the occurrences
    # of each product in the CartItem table
    product_count_query = (
        db.session.query(Product, func.count(CartItem.id).label("cart_count"))\
        .join(CartItem, Product.id == CartItem.product_id)\
        .group_by(Product.id)\
        .order_by(func.count(CartItem.id).desc())
    )

    # Execute the query
    product_count_results = product_count_query.all()
    product_count_results = [i[0] for i in product_count_results]
    if len(product_count_results) != 0:
        return product_count_results[:3]
    return []


def products_by_category(category):
    """
    Get products in a specific category.

    Args:
        category (str): The name of the category.

    Returns:
        List: A list of Product objects in the specified category.
    """
    category = Category.query.filter(Category.name.ilike(category)).first()
    if category:
        return category.products.all()
    return []


@public.route("/")
def index():
    """
    Render the homepage.

    Returns:
        str: Rendered HTML template for the homepage.
    """
    latest_products = Product.query.order_by(Product.id.desc()).all()
    trending_products = get_trending_products()

    electronics_products = products_by_category("electronics")
    stationary_products = products_by_category("stationary")
    homedecor_products = products_by_category("homedecor")

    return render_template(
        "public/home.html",
        trending_products=trending_products,
        latest_products=latest_products,
        electronics_products=electronics_products,
        stationary_products=stationary_products,
        homedecor_products=homedecor_products,
    )
