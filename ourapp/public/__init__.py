from flask import Blueprint, render_template
from flask_login import login_required

public = Blueprint("public", __name__, template_folder="templates", url_prefix="/")

@public.route("/")
def index():
    return render_template("public/home.html")
