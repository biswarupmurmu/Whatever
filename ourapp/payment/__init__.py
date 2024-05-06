from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from ourapp.payment.form import PaymentForm
from ourapp.logging_config.config import logger

payment_bp=Blueprint("payment",__name__,template_folder="templates",url_prefix="/payment")

@payment_bp.route('/', methods=["GET", "POST"])
@login_required
def payment():
    cart=current_user.cart
    if len(cart) == 0:
        logger.info("Redirecting to view cart because the cart is empty for %s(%s).",current_user.fname, current_user.id)
        return redirect(url_for("cart.view_cart"))
    if not current_user.address:
        flash(message="Address required", category="info")
        logger.info("Redirecting to view cart because the user %s(%s) has no address.",current_user.fname, current_user.id)
        return redirect(url_for("cart.view_cart"))
    cart_total = 0
    for cartItem in cart:
        cart_total += (cartItem.product.price * cartItem.quantity)

    form = PaymentForm(request.form)

    if form.validate_on_submit():
        session["payment_received"] = True
        logger.info("Payment received. Redirecting to place order.")
        return redirect(url_for("order_bp.place_order"))
    logger.info("Rendering payment page.")
    return render_template("payment/payment.html",form = form, cart_total=cart_total)
