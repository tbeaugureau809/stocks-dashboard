from flask import Blueprint, render_template
from app.services.movers_service import compute_movers
from app.db import SessionLocal
from app.models import Watchlist


bp = Blueprint("movers", __name__)

@bp.route("/movers", methods = ["GET"])
def show_movers():
    db = SessionLocal()
    movers={"top": [], "bottom": []}
    error = None

    try:
        #Currently hardcoded amount of movers to show for dashboard.
        symbols = [ w.symbol for w in db.query(Watchlist).all()]
        movers = compute_movers(symbols, 3)

    except Exception as e:
        error=f"Could not load movers; {e}"

    finally:
        db.close()

    return render_template("movers.html", movers=movers, error=error)

