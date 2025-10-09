from flask import Blueprint, render_template, request
from app.services.chart_service import plot_history_with_sma
from app.services.indicators_service import get_history_with_sma


bp = Blueprint("charts", __name__)

@bp.route("/charts", methods = ["POST"])
def show_charts():
    symbol = request.form.get("symbol")
    error = None
    image = None

    try:
        df = get_history_with_sma(symbol)

        if df is None or df.empty:
            error = f"No data available for {symbol}."
        else:
            image = plot_history_with_sma(df, symbol)

    except Exception as e:
        error=f"Could not load chart; {e}"

    return render_template("graphs.html", symbol=symbol, image=image, error=error)



