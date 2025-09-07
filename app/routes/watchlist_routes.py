from flask import Blueprint,  request, jsonify
from app.services.watchlist_service import add_symbol, delete_symbol, get_watchlist

bp = Blueprint("watchlist", __name__)

#Add a ticker to the watchlist
@bp.route("/watchlist/add", methods=["POST"])
def add_watchlist():
    symbol = request.json.get("symbol") #extract "symbol" from JSON body
    return jsonify(add_symbol(symbol)) #call service, return response

@bp.route("/watchlist/delete", methods=["POST"])
def delete_watchlist():
    symbol = request.json.get("symbol")
    return jsonify(delete_symbol(symbol))

@bp.route("/watchlist", methods=["GET"])
def watchlist_page():
    return jsonify(get_watchlist())
