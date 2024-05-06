from flask import Blueprint, render_template, redirect, url_for
from ourapp.models import Product, Category
from ourapp.logging_config.config import logger

product_bp=Blueprint("product_bp",__name__, url_prefix="/product", template_folder="templates")

@product_bp.route('/all')
def view_all_products():
    products=Product.query.all()
    logger.info("Viewing all products.")
    return render_template("product/all.html",products=products)

# View products by categories
@product_bp.route('/category/<string:category>')
def view_products_by_category(category):
    category = Category.query.filter(Category.name.ilike(category)).first()
    if category:
        products_with_categories=category.products.all()
        logger.info("Viewing products by category: %s", category)
        return render_template("product/products_by_categories.html",products=products_with_categories, category=category.name)
    else:
        logger.warning("Category not found: %s. Redirecting to view all products.", category)
        return redirect(url_for('product_bp.view_all_products'))

@product_bp.route('/<int:id>')
def view_product_details(id):
    product = Product.query.filter_by(id=id).first()
    features=product.features.split('\n')
    logger.info("Viewing details of product %s(%s).", product.name, product.id)
    return render_template("product/product_details.html", product=product,features=features)
