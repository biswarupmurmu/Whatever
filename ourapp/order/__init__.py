"""
This blueprint handles operations related to orders placed by customers.

This blueprint provides routes for placing orders, viewing orders, changing
address, providing feedback, cancelling orders, and returning orders.
"""

from random import randint
from datetime import datetime, timedelta
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    redirect,
    session,
    url_for,
    abort,
)
from flask_login import current_user, login_required
from ourapp.logging_config.config import logger
from ourapp.extensions import db
from ourapp.models import CartItem, Product, Order, OrderedItem

order_bp = Blueprint(
    "order_bp", __name__, template_folder="templates", url_prefix="/order"
)


def generate_order_id():
    """
    generates a order id
    """
    return randint(10**6, (10**7) - 1)


@order_bp.route("/place")
@login_required
def place_order():
    """
    Place an order for the items in the user's cart.

    Returns:
        Renders the acknowledgement template with the total order amount and order details.

    """
    # Ensure the cart is not empty
    # If empty return to products or say no item in the cart
    if len(current_user.cart) <= 0:
        flash(message="Cart is empty", category="info")
        return redirect(url_for("public.index"))
    # Check if payment is successful
    if "payment_received" not in session:
        flash(message="Payment unsuccessful", category="error")
        return redirect(url_for("payment.payment"))

    # Removing payment status
    session.pop("payment_received")

    customer_id = current_user.id
    arriving_date = datetime.now() + timedelta(days=7)
    while True:
        order_id = generate_order_id()
        if not Order.query.filter_by(id=order_id).first():
            break
    new_order = Order(
        id=order_id,
        customer_id=customer_id,
        arriving_date=arriving_date,
        address=current_user.address,
    )
    db.session.add(new_order)
    db.session.commit()
    print(new_order)
    for cartitem in current_user.cart:
        order_id = new_order.id
        product_id = cartitem.product.id
        quantity = cartitem.quantity
        price = cartitem.product.price
        new_ordereditem = OrderedItem(
            order_id=order_id, product_id=product_id, quantity=quantity, price=price
        )
        db.session.add(new_ordereditem)
        logger.info(
            "Order placed successfully for Customer %s(%s) Order ID: %s",
            current_user.fname,
            current_user.id,
            new_order.id,
        )
    CartItem.query.filter_by(
        customer_id=customer_id
    ).delete()  # Clearing the user's cart
    db.session.commit()
    flash(message=f"{new_order.id}", category="order_placed_success")

    return redirect(url_for("order_bp.view_orders", status="confirmed"))


@order_bp.route("/<status>")
@login_required
def view_orders(status):
    """
    View orders based on their status.

    Args:
        status (str): The status of the orders to be viewed.

    Returns:
        Renders templates based on the status of the orders.

    """
    allowed_status = set(
        ["confirmed", "cancelled", "delivered", "intransit", "returned"]
    )
    if status.lower() not in allowed_status:
        abort(404)
    orders = current_user.orders
    orders_by_status = []
    for order in orders:
        if order.status.lower() == status.lower():
            total = 0
            items = set()
            for ordered_item in order.ordered_items:
                total += ordered_item.price * ordered_item.quantity
                items.add(ordered_item.product.name)
            orders_by_status.append([order, list(items), total])
    logger.info(
        "Customer %s(%s) Viewing orders with status: %s",
        current_user.fname,
        current_user.id,
        status.lower(),
    )
    if status == "cancelled":
        return render_template(
            "order/cancelled.html", orders=orders_by_status, status=status.lower()
        )
    if status == "delivered":
        return render_template(
            "order/delivered.html", orders=orders_by_status, status=status.lower()
        )
    if status == "returned":
        return render_template(
            "order/returned.html", orders=orders_by_status, status=status.lower()
        )
    if status == "intransit":
        return render_template(
            "order/intransit.html", orders=orders_by_status, status=status.lower()
        )
    return render_template(
        "order/confirmed.html", orders=orders_by_status, status=status.lower()
    )


@order_bp.route("/<int:order_id>/change_address")
@login_required
def change_address(order_id):
    """
    Change the shipping address of an order.

    Args:
        order_id (int): The ID of the order to change the address for.

    Returns:
        Redirects to the view orders page after changing the address.

    """
    order = Order.query.filter_by(id=order_id).first()
    if order and order.customer_id == current_user.id:
        new_order_address = request.args.get("address").strip()
        if len(new_order_address) == 0:
            flash(message="Address cannot be empty", category="info")
        else:
            order.address = new_order_address
            db.session.commit()
            logger.info(
                "Address updated for customer %s(%s) for order %s. New address: %s",
                current_user.fname,
                current_user.id,
                order.id,
                new_order_address,
            )
            flash(message="Address updated successfully", category="success")
    return redirect(url_for("order_bp.view_orders", status="confirmed"))


@order_bp.route("/<int:order_id>/feedback")
@login_required
def get_feedback(order_id):
    """
    Provide feedback for a delivered order.

    Args:
        order_id (int): The ID of the delivered order to provide feedback for.

    Returns:
        Redirects to the view orders page after providing feedback.

    """
    order = Order.query.filter_by(id=order_id).first()
    if order and order.customer_id == current_user.id:
        print("ABCD")
        order.feedback = request.args.get("feedback")
        print(order.feedback)
        db.session.commit()
        logger.info(
            "Feedback added by Customer %s(%s) for order %s. Feedback: %s",
            current_user.fname,
            current_user.id,
            order.id,
            order.feedback,
        )
    return redirect(url_for("order_bp.view_orders", status="delivered"))


@order_bp.route("/<int:order_id>/cancel")
@login_required
def cancel_order(order_id):
    """
    Cancel an order.

    Args:
        order_id (int): The ID of the order to cancel.

    Returns:
        Redirects to the view orders page after cancelling the order.

    """
    order = Order.query.filter_by(id=order_id).first()
    if order and order.customer_id == current_user.id:
        order.status = "cancelled"
        order.date_according_to_status = datetime.now()
        db.session.commit()
        flash(message="Order cancelled", category="success")
        logger.info(
            "Order Cancelled successfully for Customer %s(%s) Order ID: %s",
            current_user.fname,
            current_user.id,
            order_id,
        )
    return redirect(url_for("order_bp.view_orders", status="cancelled"))


@order_bp.route("/<int:order_id>/return")
@login_required
def return_order(order_id):
    """
    Return an order.

    Args:
        order_id (int): The ID of the order to return.

    Returns:
        Redirects to the view orders page after returning the order.

    """
    order = Order.query.filter_by(id=order_id).first()
    if order and order.customer_id == current_user.id:
        order.status = "returned"
        order.date_according_to_status = datetime.now()
        db.session.commit()
        flash(message="Return requested", category="success")
        logger.info(
            "Return requested for order %s by user %s(%ss)",
            order.id,
            current_user.fname,
            current_user.id,
        )
    return redirect(url_for("order_bp.view_orders", status="returned"))
