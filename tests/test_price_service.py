from app.services import price_service
from datetime import datetime, timezone, timedelta
import pytest

def test_daily_change_positive(monkeypatch):
    price_service.change_cache.clear()
    def fake_latest_price(symbol):
        return(110,datetime(2020, 9, 26, 10, 0, 22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return 100

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result["percent_change"] == 10.0
    assert result["latest"] == 110
    assert result["previous_close"] == 100
    assert result["symbol"] == "AAPL"
    assert result["last_updated"] == datetime(2020, 9, 26, 10, 0, 22, tzinfo=timezone.utc)


def test_daily_change_negative(monkeypatch):
    price_service.change_cache.clear()
    def fake_latest_price(symbol):
        return(90, datetime(2020, 9,26, 10, 0, 22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return 100

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result["percent_change"] == (-10.0)
    assert result["latest"] == 90
    assert result["previous_close"] == 100
    assert result["symbol"] == "AAPL"
    assert result["last_updated"] == datetime(2020, 9,26,10, 0, 22, tzinfo=timezone.utc)


def test_daily_change_no_change(monkeypatch):
    price_service.change_cache.clear()

    def fake_latest_price(symbol):
        return(100,datetime(2020, 9, 26, 10, 0, 22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return 100

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result["percent_change"] == 0.0
    assert result["latest"] == 100
    assert result["previous_close"] == 100
    assert result["symbol"] == "AAPL"
    assert result["last_updated"] == datetime(2020, 9, 26, 10, 0, 22, tzinfo=timezone.utc)

def test_daily_change_divided_by_zero(monkeypatch):
    price_service.change_cache.clear()
    def fake_latest_price(symbol):
        return(100, datetime(2020,9,26,10,0,22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return 0

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result is None

def test_daily_change_latest_none(monkeypatch):
    price_service.change_cache.clear()

    def fake_latest_price(symbol):
        return(None, datetime(2020, 9,26,10,0,22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return 100

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result == None

def test_daily_change_prev_none(monkeypatch):
    price_service.change_cache.clear()

    def fake_latest_price(symbol):
        return(100, datetime(2020,9,26,10,0,22, tzinfo=timezone.utc))

    def fake_previous_close(symbol):
        return None

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result == None

def test_daily_change_stale(monkeypatch):
    price_service.change_cache.clear()

    def fake_latest_price(symbol):
        old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        return(100, old_time)

    def fake_previous_close(symbol):
        return 100

    monkeypatch.setattr(price_service, "latest_price", fake_latest_price)
    monkeypatch.setattr(price_service, "previous_close", fake_previous_close)

    result = price_service.daily_change("AAPL")

    assert result["stale"] == True

