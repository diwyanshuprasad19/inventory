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
        client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 999999}).status_code == 409
    )
    assert client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 0}).status_code == 422
    assert client.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 1}).status_code == 200


def test_empty_and_malformed_body(client):
    assert client.post(
        "/v1/stock/reserve", content=b"", headers={"content-type": "application/json"}
    ).status_code in {
        400,
        422,
    }
    assert client.post(
        "/v1/stock/reserve",
        content=b"{not-json",
        headers={"content-type": "application/json"},
    ).status_code in {400, 422}


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


def test_ready_metrics_seed_lists(client):
    assert client.get("/ready").status_code == 200
    assert client.get("/metrics").status_code == 200
    assert "inventory_http_requests_total" in client.get("/metrics").text
    seeded = client.post("/v1/seed")
    assert seeded.status_code == 200
    assert client.get("/v1/warehouses").status_code == 200
    assert client.get("/v1/stock").status_code == 200
    assert client.get("/v1/reservations").status_code == 200
    assert client.get("/v1/movements").status_code == 200
    assert client.get("/v1/suppliers").status_code == 200
    assert client.get("/v1/categories").status_code == 200


def test_sku_crud_and_stock_by_sku(client):
    created = client.post(
        "/v1/skus",
        json={"sku": "TEST-SKU-X", "name": "Test SKU", "unit_cost_cents": 10},
    )
    assert created.status_code == 201
    assert (
        client.post(
            "/v1/skus",
            json={"sku": "TEST-SKU-X", "name": "Dup"},
        ).status_code
        == 409
    )
    got = client.get("/v1/skus/TEST-SKU-X")
    assert got.status_code == 200
    assert got.json()["name"] == "Test SKU"
    assert client.get("/v1/skus/NO-SUCH").status_code == 404
    patched = client.patch("/v1/skus/TEST-SKU-X", json={"name": "Renamed", "status": "active"})
    assert patched.status_code == 200
    assert patched.json()["name"] == "Renamed"
    assert client.patch("/v1/skus/NO-SUCH", json={"name": "x"}).status_code == 404
    # new sku has no stock rows yet
    assert client.get("/v1/stock/TEST-SKU-X").status_code == 404
    assert client.get("/v1/stock/WIDGET-1").status_code == 200


def test_warehouse_supplier_create(client):
    wh = client.post("/v1/warehouses", json={"code": "WH-TEST", "name": "Test WH", "region": "EU"})
    assert wh.status_code == 201
    assert wh.json()["code"] == "WH-TEST"
    sup = client.post(
        "/v1/suppliers",
        json={"code": "SUP-T", "name": "Supplier T", "email": "t@example.com"},
    )
    assert sup.status_code == 201


def test_adjust_transfer_happy_and_edges(client):
    ok = client.post(
        "/v1/stock/adjust",
        json={"sku": "WIDGET-1", "warehouse_code": "WH-EAST", "delta": 5, "reason": "audit"},
    )
    assert ok.status_code == 200
    assert ok.json()["quantity"] >= 5
    bad_adj = client.post(
        "/v1/stock/adjust",
        json={"sku": "WIDGET-1", "warehouse_code": "WH-EAST", "delta": -999999, "reason": "x"},
    )
    assert bad_adj.status_code == 409
    xfer = client.post(
        "/v1/stock/transfer",
        json={
            "sku": "WIDGET-1",
            "from_warehouse": "WH-EAST",
            "to_warehouse": "WH-WEST",
            "qty": 1,
        },
    )
    assert xfer.status_code == 200
    assert "from" in xfer.json() and "to" in xfer.json()
    assert (
        client.post(
            "/v1/stock/transfer",
            json={
                "sku": "NOPE",
                "from_warehouse": "WH-EAST",
                "to_warehouse": "WH-WEST",
                "qty": 1,
            },
        ).status_code
        == 404
    )
    assert (
        client.post(
            "/v1/stock/transfer",
            json={
                "sku": "WIDGET-1",
                "from_warehouse": "WH-EAST",
                "to_warehouse": "WH-WEST",
                "qty": 999999,
            },
        ).status_code
        == 409
    )


def test_reserve_with_warehouse_and_legacy_reserve(client):
    held = client.post(
        "/v1/stock/reserve",
        json={"sku": "WIDGET-1", "qty": 1, "warehouse_code": "WH-EAST", "order_ref": "ord-1"},
    )
    assert held.status_code == 200
    rid = held.json()["reservation_id"]
    assert client.post("/v1/stock/release", json={"reservation_id": rid}).status_code == 200
    legacy = client.post("/reserve", json={"sku": "WIDGET-2", "qty": 1})
    assert legacy.status_code == 200
    assert "reservation_id" in legacy.json()
    assert client.post("/reserve", json={"sku": "NOPE", "qty": 1}).status_code == 404


def test_get_db_generator_and_service_create_stock():
    """Exercise get_db finally-close and get_or_create_stock create path."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from inventory_app import models, services
    from inventory_app.db import Base, get_db

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()
    wh = models.Warehouse(code="W1", name="One", region="US")
    db.add(wh)
    db.add(models.Sku(sku="S1", name="Sku1"))
    db.commit()
    db.refresh(wh)
    stock = services.get_or_create_stock(db, "S1", wh.id)
    assert stock.quantity == 0
    again = services.get_or_create_stock(db, "S1", wh.id)
    assert again.id == stock.id
    db.close()
    # generator close path
    gen = get_db()
    next(gen)
    gen.close()


def test_reserve_no_warehouses_raises():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from inventory_app import models, services
    from inventory_app.db import Base

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()
    db.add(models.Sku(sku="ONLY", name="Only"))
    db.commit()
    with pytest.raises(services.InventoryError) as ei:
        services.reserve(db, "ONLY", 1, None, None)
    assert ei.value.code == 409
    db.close()


def test_transfer_qty_nonpositive_and_main(monkeypatch):
    import uvicorn
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    import inventory_app.app as app_mod
    from inventory_app import models, services
    from inventory_app.db import Base

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()
    db.add(models.Sku(sku="S", name="S"))
    db.add(models.Warehouse(code="A", name="A"))
    db.add(models.Warehouse(code="B", name="B"))
    db.commit()
    with pytest.raises(services.InventoryError):
        services.transfer(db, "S", "A", "B", 0)
    db.close()

    ran = {}

    def fake_run(*a, **k):
        ran["ok"] = True

    monkeypatch.setattr(uvicorn, "run", fake_run)
    app_mod.main()
    assert ran.get("ok") is True
