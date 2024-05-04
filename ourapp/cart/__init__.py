from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from ourapp import db
from ourapp.models import CartItem, Product

cart_bp=Blueprint("cart",__name__,template_folder="templates",url_prefix="/cart")



@cart_bp.route("/add-to-cart/<int:id>")
@login_required
def add_to_cart(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(product_id=id, customer_id=current_user.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            new_cart_item = CartItem(product_id=id, customer_id=current_user.id)
            db.session.add(new_cart_item)
        db.session.commit()

        for cartitem in current_user.cart:
            print(cartitem.product, cartitem.quantity)
        
    return redirect(url_for('cart.view_cart'))

@cart_bp.route("/")
@login_required
def view_cart():
    cart=current_user.cart
    cart_total = 0
    for cartItem in cart:
        cart_total += (cartItem.product.price * cartItem.quantity)
    return render_template("cart/view_cart.html",cart=cart, cart_total=cart_total)

@cart_bp.route('/increment/<int:id>')
@login_required
def increment(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(product_id=id, customer_id=current_user.id).first()
        if cart_item:
            cart_item.quantity += 1
            db.session.commit()
    return redirect(url_for('cart.view_cart'))
    
@cart_bp.route('/decrement/<int:id>')
@login_required
def decrement(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(product_id=id, customer_id=current_user.id).first()
        if cart_item:
            cart_item.quantity -= 1
            if cart_item.quantity ==0:
                return redirect(url_for('cart.remove',id=product.id))
            db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:id>')
@login_required
def remove(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        # Check if product is already in the cart
        cart_item = CartItem.query.filter_by(product_id=id, customer_id=current_user.id).first()
        if cart_item:
            CartItem.query.filter_by(product_id=id, customer_id=current_user.id).delete()
            db.session.commit()
    return redirect(url_for('cart.view_cart'))
            
