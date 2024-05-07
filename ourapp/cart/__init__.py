"""
This blueprint handles operations related to the shopping cart.

This blueprint provides routes for adding products to the cart, viewing the cart,
updating the quantity of items in the cart, and removing items from the cart.
"""

from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ourapp.extensions import db
from ourapp.models import CartItem, Product
from ourapp.logging_config.config import logger

cart_bp = Blueprint("cart", __name__, template_folder="templates", url_prefix="/cart")


@cart_bp.route("/add-to-cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    """
    Add a product to the shopping cart.

    Args:
        id (int): The ID of the product to add to the cart.

    Returns:
        Redirects to the view cart page after adding the product to the cart.

    """
    product = Product.query.filter_by(id=product_id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(
            product_id=product_id, customer_id=current_user.id
        ).first()
        if cart_item:
            cart_item.quantity += 1
            logger.info(
                "Incremented quantity of product %s(%s) in the cart for user %s(%s)",
                product.name,
                product.id,
                current_user.fname,
                current_user.id,
            )
        else:
            new_cart_item = CartItem(product_id=product_id, customer_id=current_user.id)
            db.session.add(new_cart_item)
            logger.info(
                "Added product %s(%s) to the cart for user %s(%s)",
                product.name,
                product.id,
                current_user.fname,
                current_user.id,
            )
        db.session.commit()
        flash(message="Product added to the cart!", category="success")
        logger.info(
            "Product %s(%s) added to the cart for user %s(%s)",
            product.id,
            product.name,
            current_user.fname,
            current_user.id,
        )

    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/")
@login_required
def view_cart():
    """
    View the contents of the shopping cart.

    Returns:
        Renders the view cart template with the cart items and total cart value.

    """
    cart = current_user.cart
    cart_total = 0
    for cartitem in cart:
        cart_total += cartitem.product.price * cartitem.quantity
        logger.info("Viewing cart for user %s(%s)", current_user.fname, current_user.id)
    return render_template("cart/view_cart.html", cart=cart, cart_total=cart_total)


@cart_bp.route("/increment/<int:product_id>")
@login_required
def increment(product_id):
    """
    Increment the quantity of a product in the shopping cart.

    Args:
        id (int): The ID of the product to increment the quantity of.

    Returns:
        Redirects to the view cart page after incrementing the quantity.

    """
    product = Product.query.filter_by(id=product_id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(
            product_id=product_id, customer_id=current_user.id
        ).first()
        if cart_item:
            cart_item.quantity += 1
            db.session.commit()
            logger.info(
                "Incremented quantity of product %s(%s) in the cart for user %s(%s)",
                product.name,
                product.id,
                current_user.fname,
                current_user.id,
            )
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/decrement/<int:product_id>")
@login_required
def decrement(product_id):
    """
    Decrement the quantity of a product in the shopping cart.

    Args:
        id (int): The ID of the product to decrement the quantity of.

    Returns:
        Redirects to the view cart page after decrementing the quantity. If the
        quantity becomes zero, the item is removed from the cart.

    """
    product = Product.query.filter_by(id=product_id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(
            product_id=product_id, customer_id=current_user.id
        ).first()
        if cart_item:
            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                return redirect(url_for("cart.remove", product_id=product.id))
            db.session.commit()
            logger.info(
                "Decremented quantity of product %s(%s) in the cart for user %s(%s)",
                product.name,
                product.id,
                current_user.fname,
                current_user.id,
            )
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove/<int:product_id>")
@login_required
def remove(product_id):
    """
    Remove a product from the shopping cart.

    Args:
        id (int): The ID of the product to remove from the cart.

    Returns:
        Redirects to the view cart page after removing the product from the cart.

    """
    product = Product.query.filter_by(id=product_id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(
            product_id=product_id, customer_id=current_user.id
        ).first()
        if cart_item:
            CartItem.query.filter_by(
                product_id=product_id, customer_id=current_user.id
            ).delete()
            db.session.commit()
            logger.info(
                "Removed product %s(%s) from the cart for user %s(%s)",
                product.name,
                product.id,
                current_user.fname,
                current_user.id,
            )
    return redirect(url_for("cart.view_cart"))
