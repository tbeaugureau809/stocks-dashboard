import yfinance as yf
from app.db import SessionLocal
from app.models import Watchlist



#Validate whether ticker exists
def validate_symbol(symbol: str) -> bool:
    data = yf.Ticker(symbol).history(period="1d")
    return not data.empty

#Check if symbol already exists in DB
def exists_symbol(session, symbol: str) -> bool:
    return session.query(Watchlist).filter(Watchlist.symbol == symbol).first() is not None


#Add symbol
def add_symbol(symbol: str):
    if not validate_symbol(symbol):
        return {"error": f"{symbol} is invalid"}

    session = SessionLocal()

    try:
        if exists_symbol(session, symbol):
            return{"error": f"{symbol} has already been added"}

        new_symbol = Watchlist(symbol=symbol)
        session.add(new_symbol)
        session.commit()
        return {"message": f"{symbol} added to watchlist"}

    finally:
        session.close()

#Delete symbol
def delete_symbol(symbol: str):
    session = SessionLocal()

    try:
        row = session.query(Watchlist).filter(Watchlist.symbol == symbol).first()

        if not row:
            return {"error": f"{symbol} is not on current watchlist"}

        session.delete(row)
        session.commit()
        return {"message": f"{symbol} was deleted from watchlist"}

    finally:
        session.close()

#Get current watchlist
def get_watchlist():
    session = SessionLocal()
    symbols = [row.symbol for row in session.query(Watchlist).all()]

    session.close()
    return symbols

