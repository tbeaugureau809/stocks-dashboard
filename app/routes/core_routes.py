from flask import Blueprint, render_template, jsonify, redirect, url_for

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return redirect("/watchlist")

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})
