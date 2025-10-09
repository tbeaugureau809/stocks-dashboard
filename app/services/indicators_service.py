from app.services.price_service import fetch_with_retry
import yfinance as yf

def symbol_history(symbol: str, interval: str, days: int = 20, retries=3):
    period = f"{days}d"
    data = fetch_with_retry(symbol, period=period, interval=interval)
    if data is None or data.empty:
        return None
    return data["Close"].iloc[-days:]

def get_history_with_sma(symbol: str, days: int = 60, interval: str = "1d"):
    period = f"{days}d"
    data = fetch_with_retry(symbol, period=period, interval=interval)

    if data is None or data.empty:
        return None

    df = data[["Close"]].copy()

    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()

    return df

def get_fast_info(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.fast_info
    return {
        "market_cap": info.get("market_cap"),
        "pe_ratio": info.get("trailing_pe"),
        "dividend_yield": info.get("dividend_yield"),
        "currency": info.get("currency")

    }
