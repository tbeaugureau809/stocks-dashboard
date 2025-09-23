from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base
from app.db import Base



class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, unique=True)

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class JobRun(Base):
    __tablename__ = "jobs_run"
    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False)
    run_time = Column(DateTime, nullable=False)

class PriceHistory(Base):
    __tablename__ = "price_history"

    symbol = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)



