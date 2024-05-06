from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from ourapp.payment.form import PaymentForm

payment_bp=Blueprint("payment",__name__,template_folder="templates",url_prefix="/payment")

@payment_bp.route('/', methods=["GET", "POST"])
@login_required
def payment():
    """
    Render the payment page and handle payment processing.

    If the user is not logged in, they will be redirected to the login page.
    If the user's cart is empty, they will be redirected to view their cart.
    If the user does not have an address set, a flash message will inform them and redirect to view their cart.
    The total price of items in the cart is calculated.
    If the payment form is submitted and validated, the session variable "payment_received" is set to True,
    and the user is redirected to place their order.

    Returns:
        str: Rendered HTML template for the payment page.
    """
    cart=current_user.cart
    if len(cart) == 0:
        return redirect(url_for("cart.view_cart"))
    if not current_user.address:
        flash(message="Address required", category="info")
        return redirect(url_for("cart.view_cart"))
    cart_total = 0
    for cartItem in cart:
        cart_total += (cartItem.product.price * cartItem.quantity)

    form = PaymentForm(request.form)

    if form.validate_on_submit():
        session["payment_received"] = True
        return redirect(url_for("order_bp.place_order"))

    return render_template("payment/payment.html",form = form, cart_total=cart_total)
