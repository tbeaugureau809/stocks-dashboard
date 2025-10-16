from flask import Blueprint,  request, render_template, redirect, url_for, flash
from app.services.watchlist_service import add_symbol, delete_symbol
from app.services.price_service import latest_price

bp = Blueprint("watchlist", __name__)

#Add a ticker to the watchlist
@bp.route("/watchlist/add", methods=["POST"])
def add_watchlist():
    symbol = request.form.get("symbol")

    if not symbol:
        flash("Please enter a ticker symbol", "danger")
        return redirect(url_for("watchlist.watchlist_page"))

    result = add_symbol(symbol)

    if "error" in result:
        flash(result["error"], "danger")
    else:
        flash(result["message"], "success")


    return redirect(url_for("watchlist.watchlist_page"))

@bp.route("/watchlist/delete", methods=["POST"])
def delete_watchlist():
    symbol = request.form.get("symbol")
    result = delete_symbol(symbol)

    if "error" in result:
        flash(result["error"], "danger")
    else:
        flash(result["message"], "success")

    return redirect(url_for("watchlist.watchlist_page"))


from app.services.price_service import latest_price
from app.db import SessionLocal
from app.models import Watchlist

@bp.route("/watchlist", methods=["GET"])
def watchlist_page():
    session = SessionLocal()
    symbols = session.query(Watchlist).all()

    results = []
    for w in symbols:
        price, _ = latest_price(w.symbol)
        results.append({
            "symbol": w.symbol,
            "price": price
        })

    session.close()
    return render_template("watchlist.html", symbols=results)
