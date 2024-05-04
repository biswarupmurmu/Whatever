from flask import Blueprint, render_template
from flask_login import login_required
from ourapp.models import Product

public = Blueprint("public", __name__, template_folder="templates", url_prefix="/")

@public.route("/")
def index():
    trending_products=Product.query.all()
    print(trending_products)
    return render_template("public/home.html",trending_products=trending_products)

