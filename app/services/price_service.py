import yfinance as yf
from cachetools import TTLCache, cached
import time

latest_cache = TTLCache(maxsize=500, ttl=60)
prev_cache = TTLCache(maxsize=500, ttl=60)
change_cache= TTLCache(maxsize=500, ttl=60)

price_cache = TTLCache(maxsize=500, ttl=60)

def fetch_with_retry(symbol: str, period: str, interval: str, retries=3):
    for attempt in range(retries):
        try:
            data = yf.Ticker(symbol).history(period=period, interval=interval)
            if not data.empty:
                return data
        except Exception as e:
            print(f"Error fetching {symbol} (attempt {attempt+1}): {e}")
        time.sleep(0.5*(attempt+1))
    return None

@cached(latest_cache)
def latest_price(symbol: str) -> float | None:

    data = fetch_with_retry(symbol, period="1d", interval="1m")
    if data is None:
        return None
    return float(data["Close"].iloc[-1])

@cached(prev_cache)
def previous_close(symbol: str) -> float | None:
    data = fetch_with_retry(symbol, period="2d", interval="1d")
    if data is None or len(data) < 2:
        return None
    return float(data["Close"].iloc[-2])

@cached(change_cache)
def daily_change(symbol: str) -> dict | None:
    latest = latest_price(symbol)
    prev = previous_close(symbol)

    if latest is None or prev is None:
        return None

    change = ((latest-prev)/prev)*100

    return {
        "symbol": symbol,
        "latest": latest,
        "previous_close": prev,
        "percent_change": round(change, 2)
    }

