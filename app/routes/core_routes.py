from flask import Blueprint, jsonify, redirect

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return redirect("/watchlist")

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})
