import pytest
from app import create_app

def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b"ok" in response.data

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/watchlist")

def test_watchlist_add(client):
    response = client.post(
    "/watchlist/add",
    data = {"symbol": "AAPL"},
    follow_redirects=True
    )
    assert response.status_code == 200
    assert b"AAPL" in response.data or b"added" in response.data

def test_watchlist_delete(client):
    response = client.post(
        "/watchlist/add",
        data = {"symbol": "AAPL"},
        follow_redirects=True
    )
    response = client.post(
        "/watchlist/delete",
        data = {"symbol": "AAPL"},
        follow_redirects=True
        )
    assert response.status_code == 200
    assert b"was deleted from watchlist" in response.data

def test_watchlist(client):
    response = client.get(
        "/watchlist",
        follow_redirects=True
    )
    assert response.status_code == 200
