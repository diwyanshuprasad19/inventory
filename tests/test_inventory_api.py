import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use in-memory sqlite for unit tests
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
        # seed via override session
        db = Session()
        seed_demo(db)
        db.close()
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200


def test_list_skus_after_seed(client):
    # re-seed through API using app db — create fresh
    pass


def test_reserve_edge_cases():
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
        assert c.get("/v1/skus").status_code == 200
        assert len(c.get("/v1/skus").json()) >= 10
        bad = c.post("/v1/stock/reserve", json={"sku": "NOPE", "qty": 1})
        assert bad.status_code == 404
        over = c.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 999999})
        assert over.status_code == 409
        ok = c.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 1})
        assert ok.status_code == 200
        zero = c.post("/v1/stock/reserve", json={"sku": "WIDGET-1", "qty": 0})
        assert zero.status_code == 422
