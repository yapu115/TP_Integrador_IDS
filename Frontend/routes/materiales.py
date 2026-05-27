from flask import Blueprint, render_template

materiales_bp = Blueprint("materiales", __name__)

@materiales_bp.route("/materiales")
def materiales():
    return render_template("materiales.html")
