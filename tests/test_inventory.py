"""Inventory API + store edge cases."""

from __future__ import annotations

import pytest

from inventory_app.app import create_app
from inventory_app.store import InventoryStore, StockError


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_stock_ok(client) -> None:
    r = client.get("/stock/sku-100")
    assert r.status_code == 200
    assert r.get_json()["available"] == 50


def test_stock_unknown(client) -> None:
    assert client.get("/stock/missing").status_code == 404


def test_stock_fully_reserved(client) -> None:
    r = client.get("/stock/sku-300")
    assert r.status_code == 200
    assert r.get_json()["available"] == 0


def test_reserve_ok(client) -> None:
    r = client.post("/reserve", json={"sku": "sku-100", "qty": 2})
    assert r.status_code == 200
    assert r.get_json()["status"] == "reserved"


def test_reserve_insufficient(client) -> None:
    r = client.post("/reserve", json={"sku": "sku-200", "qty": 1})
    assert r.status_code == 409


def test_reserve_bad_qty(client) -> None:
    r = client.post("/reserve", json={"sku": "sku-100", "qty": 0})
    assert r.status_code == 409


def test_store_release_edge() -> None:
    s = InventoryStore()
    s.reserve("sku-100", 5)
    item = s.release("sku-100", 100)  # over-release clamps
    assert item.reserved == 0
    with pytest.raises(StockError):
        s.get("nope")
