"""Inventory API edge cases — matrix rows: validation, not-found, conflict, release, transfer, telemetry."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from inventory_app.app import create_app
from inventory_app.db import Base, get_db
from inventory_app.seed import seed_demo


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def _get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        db = Session()
        seed_demo(db)
        db.close()
        yield c


def test_health_and_telemetry_safe(client):
    assert client.get("/health").status_code == 200
    tel = client.get("/v1/telemetry")
    assert tel.status_code == 200
    body = tel.json()
    assert "tracing_configured" in body
    blob = tel.text.lower()
    assert "password" not in blob and "secret" not in blob


def test_list_skus_seeded(client):
    r = client.get("/v1/skus")
    assert r.status_code == 200
    assert len(r.json()) >= 10


def test_reserve_unknown_over_zero(client):
    assert client.post("/v1/stock/reserve", json={"sku": "NOPE", "qty": 1}).status_code == 404
    assert (
        client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 999999}).status_code
        == 409
    )
    assert client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 0}).status_code == 422
    assert client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 1}).status_code == 200


def test_empty_and_malformed_body(client):
    assert client.post("/v1/stock/reserve", content=b"", headers={"content-type": "application/json"}).status_code in {
        400,
        422,
    }
    assert (
        client.post(
            "/v1/stock/reserve",
            content=b"{not-json",
            headers={"content-type": "application/json"},
        ).status_code
        in {400, 422}
    )


def test_release_unknown_and_double_release(client):
    bad = client.post("/v1/stock/release", json={"reservation_id": "missing"})
    assert bad.status_code == 404
    held = client.post("/v1/stock/reserve", json={"sku": "WIDGET-2", "qty": 1})
    assert held.status_code == 200
    rid = held.json()["reservation_id"]
    assert client.post("/v1/stock/release", json={"reservation_id": rid}).status_code == 200
    again = client.post("/v1/stock/release", json={"reservation_id": rid})
    assert again.status_code == 409


def test_transfer_same_and_unknown_warehouse(client):
    same = client.post(
        "/v1/stock/transfer",
        json={
            "sku": "CABLE-USB-C",
            "from_warehouse": "WH-EAST",
            "to_warehouse": "WH-EAST",
            "qty": 1,
        },
    )
    assert same.status_code == 400
    unknown = client.post(
        "/v1/stock/transfer",
        json={
            "sku": "CABLE-USB-C",
            "from_warehouse": "WH-EAST",
            "to_warehouse": "WH-NOPE",
            "qty": 1,
        },
    )
    assert unknown.status_code == 404


def test_adjust_unknown_sku(client):
    r = client.post(
        "/v1/stock/adjust",
        json={"sku": "NOPE", "warehouse_code": "WH-EAST", "delta": 1},
    )
    assert r.status_code == 404


def test_legacy_stock_alias(client):
    r = client.get("/stock/WIDGET-1")
    assert r.status_code == 200
    assert r.json()["available"] >= 0
    missing = client.get("/stock/DOES-NOT-EXIST")
    assert missing.status_code == 200
    assert missing.json().get("error") == "not_found"
