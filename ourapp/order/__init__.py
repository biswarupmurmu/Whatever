from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ourapp import db
from ourapp.models import CartItem, Product, Order, OrderedItem
from datetime import datetime, timedelta

order_bp=Blueprint("order_bp",__name__, template_folder="templates",url_prefix="/order")

@order_bp.route("/place")
@login_required
def place_order():
    # Ensure the cart is not empty
    # If empty return to products or say no item in the cart
    if len(current_user.cart) <= 0:
        # print(current_user.cart)
        return "No items in the cart"
    # print(current_user.cart)
    customer_id=current_user.id
    arriving_date=datetime.now()+timedelta(days=7)
    new_order=Order(customer_id=customer_id, arriving_date=arriving_date, address=current_user.address)
    db.session.add(new_order)
    db.session.commit()
    print(new_order)
    for cartItem in current_user.cart:
        order_id=new_order.id
        product_id=cartItem.product.id
        quantity=cartItem.quantity
        price = cartItem.product.price
        new_orderedItem=OrderedItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
        db.session.add(new_orderedItem)
    CartItem.query.filter_by(customer_id=customer_id).delete() # Clearing the user's cart
    db.session.commit()
    total=0
    # for order in current_user.orders:
    #     for orderedItem in order.ordered_items:
    #         print(orderedItem.product,orderedItem.product.price,orderedItem.quantity)
    #         total+=(orderedItem.product.price*orderedItem.quantity)
    for orderedItem in new_order.ordered_items:
        print(orderedItem.product,orderedItem.product.price,orderedItem.quantity)
        total+=(orderedItem.product.price*orderedItem.quantity)
            
    return render_template("order/acknowledgement.html", total=total, order=new_order)

@order_bp.route('/<status>')
@login_required
def view_orders(status):
    orders=current_user.orders
    
    orders_by_status = []
    for order in orders:
        if order.status.lower() == status.lower():
            total = 0
            items = set()
            for ordered_item in order.ordered_items:
                total += (ordered_item.price * ordered_item.quantity)
                items.add(ordered_item.product.name)
            orders_by_status.append([order,list(items), total])

    print(*orders_by_status)

    return render_template("order/view_orders.html",orders=orders_by_status ,status=status.lower())
    return render_template("order/view_orders.html",orders=orders, status=status.lower())
