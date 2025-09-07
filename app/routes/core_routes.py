from flask import Blueprint, render_template, jsonify

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return render_template("base.html")

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})
