from datetime import date, timedelta, timezone, datetime
from typing import Iterable, List, Dict, Any
import yfinance as yf

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db import SessionLocal
from app.models import PriceHistory, Watchlist, JobRun

def _now_utc_date() -> date:
    return datetime.now(timezone.utc).date()

def _symbols(db) -> List[str]:
    return [w.symbol for w in db.query(Watchlist).all()]

def _latest_day_in_db(db, symbol: str) -> date | None:
    return db.query(func.max(PriceHistory.date)).filter(PriceHistory.symbol == symbol).scalar()

def fetch_ohlcv(symbol: str, start: date, end: date | None=None):
    kwargs = {"interval": "1d", "start": start.isoformat()}
    if end is not None:
        kwargs["end"] = end.isoformat()
    df = yf.Ticker(symbol).history(**kwargs)
    if df is None or df.empty:
        return df
    if getattr(df.index,"tz", None) is not None:
        df = df.tz_convert("UTC")
    df.index = df.index.date
    return df

def upsert_rows(db, rows: Iterable[Dict[str, Any]]):
    if not rows:
        return
    stmt = pg_insert(PriceHistory.__table__).values(list(rows))
    update_cols = {
        c.name: getattr(stmt.excluded, c.name)
        for c in PriceHistory.__table__.columns
        if c.name not in ("symbol","date")
    }

    stmt = stmt.on_conflict_do_update(
        index_elements=["symbol", "date"],
        set_=update_cols
    )
    db.execute(stmt)

def backfill_history(days_buffer: int = 3, min_lookback_days: int = 400) -> dict:
    report = {"symbols": 0, "inserted": 0, "skipped": 0}
    db = SessionLocal()
    try:
        syms = _symbols(db)
        report["symbols"] = len(syms)
        today = _now_utc_date()

        for sym in syms:
            latest = _latest_day_in_db(db, sym)
            if latest:
                start = max(date(1970, 1, 1), latest - timedelta(days=days_buffer))
            else:
                start = today - timedelta(days=min_lookback_days)

            df = fetch_ohlcv(sym, start=start, end=today + timedelta(days=1))
            if df is None or df.empty:
                report["skipped"] += 1
                continue

            rows = []
            for d, row in df.iterrows():
                rows.append(
                    {
                        "symbol": sym,
                        "date": d,
                        "open": float(row["Open"]) if row["Open"] == row["Open"] else None,
                        "high": float(row["High"]) if row["High"] == row["High"] else None,
                        "low": float(row["Low"]) if row["Low"] == row["Low"] else None,
                        "close": float(row["Close"]) if row["Close"] == row["Close"] else None,
                        "volume": int(row["Volume"]) if row["Volume"] ==row["Volume"] else None

                    }
                )
            upsert_rows(db, rows)
            report["inserted"] += len(rows)

        db.add(JobRun(job_name = "nightly_backfill", run_time=func.now()))
        db.commit()
        return report
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

