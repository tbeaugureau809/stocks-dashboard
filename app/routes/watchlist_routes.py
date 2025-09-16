from flask import Blueprint,  request, render_template, redirect, url_for, flash
from app.services.watchlist_service import add_symbol, delete_symbol, get_watchlist

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


@bp.route("/watchlist", methods=["GET"])
def watchlist_page():
    symbols = get_watchlist()
    return render_template("watchlist.html", symbols = symbols)
