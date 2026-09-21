from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from sqlalchemy import select, text
from sqlalchemy.orm import Session

_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from inventory_app import models, schemas, services
from inventory_app.db import get_db
from inventory_app.seed import seed_demo
from inventory_app.settings import get_settings

try:
    from distributed_tracing import (
        configure_tracing,
        instrument_fastapi,
        telemetry_status,
    )
    from distributed_tracing.httpx_otel import instrument_httpx
    from distributed_tracing.logging_otel import configure_logging_otel
    from distributed_tracing.sqlalchemy_otel import instrument_sqlalchemy

    from inventory_app.db import engine as _engine
except ImportError:  # pragma: no cover
    configure_tracing = None
    instrument_fastapi = None
    telemetry_status = lambda: {"tracing_configured": False}  # type: ignore
    instrument_httpx = lambda: None  # type: ignore
    instrument_sqlalchemy = lambda engine=None: None  # type: ignore
    configure_logging_otel = lambda: None  # type: ignore
    _engine = None

REQ = Counter("inventory_http_requests_total", "HTTP requests", ["route", "code"])

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title="Inventory Service", version="0.2.0")
    if configure_tracing:
        os.environ.setdefault("OTEL_SERVICE_NAME", settings.otel_service_name)
        os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", settings.otel_exporter_otlp_endpoint)
        configure_tracing(settings.otel_service_name)
        configure_logging_otel()
        instrument_httpx()
        if _engine is not None:
            instrument_sqlalchemy(_engine)
        instrument_fastapi(app, service_name=settings.otel_service_name)

    @app.get("/health")
    def health():
        REQ.labels("/health", "200").inc()
        return {"status": "ok", "service": "inventory"}

    @app.get("/ready")
    def ready(db: Session = Depends(get_db)):
        db.execute(text("SELECT 1"))
        REQ.labels("/ready", "200").inc()
        return {"status": "ready"}

    @app.get("/v1/skus", response_model=list[schemas.SkuOut])
    def list_skus(db: Session = Depends(get_db)):
        rows = db.scalars(select(models.Sku).limit(500)).all()
        return rows

    @app.post("/v1/skus", response_model=schemas.SkuOut, status_code=201)
    def create_sku(body: schemas.SkuCreate, db: Session = Depends(get_db)):
        if db.get(models.Sku, body.sku):
            raise HTTPException(409, "sku exists")
        row = models.Sku(**body.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @app.get("/v1/skus/{sku}", response_model=schemas.SkuOut)
    def get_sku(sku: str, db: Session = Depends(get_db)):
        row = db.get(models.Sku, sku)
        if not row:
            raise HTTPException(404, "not found")
        return row

    @app.patch("/v1/skus/{sku}", response_model=schemas.SkuOut)
    def patch_sku(sku: str, body: schemas.SkuUpdate, db: Session = Depends(get_db)):
        row = db.get(models.Sku, sku)
        if not row:
            raise HTTPException(404, "not found")
        for k, v in body.model_dump(exclude_unset=True).items():
            setattr(row, k, v)
        db.commit()
        db.refresh(row)
        return row

    @app.get("/v1/warehouses", response_model=list[schemas.WarehouseOut])
    def list_wh(db: Session = Depends(get_db)):
        return db.scalars(select(models.Warehouse)).all()

    @app.post("/v1/warehouses", response_model=schemas.WarehouseOut, status_code=201)
    def create_wh(body: schemas.WarehouseCreate, db: Session = Depends(get_db)):
        row = models.Warehouse(**body.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @app.get("/v1/stock", response_model=list[schemas.StockOut])
    def list_stock(db: Session = Depends(get_db)):
        rows = db.scalars(select(models.StockLevel).limit(1000)).all()
        return [
            schemas.StockOut(
                sku=r.sku,
                warehouse_id=r.warehouse_id,
                quantity=r.quantity,
                reserved=r.reserved,
                available=r.available,
            )
            for r in rows
        ]

    @app.get("/v1/stock/{sku}", response_model=list[schemas.StockOut])
    def stock_sku(sku: str, db: Session = Depends(get_db)):
        rows = db.scalars(select(models.StockLevel).where(models.StockLevel.sku == sku)).all()
        if not rows:
            raise HTTPException(404, "not found")
        return [
            schemas.StockOut(
                sku=r.sku,
                warehouse_id=r.warehouse_id,
                quantity=r.quantity,
                reserved=r.reserved,
                available=r.available,
            )
            for r in rows
        ]

    @app.post("/v1/stock/reserve")
    def reserve(body: schemas.ReserveIn, db: Session = Depends(get_db)):
        try:
            res, stock = services.reserve(
                db, body.sku, body.qty, body.warehouse_code, body.order_ref
            )
        except services.InventoryError as e:
            raise HTTPException(e.code, str(e)) from e
        return {
            "reservation_id": res.id,
            "sku": stock.sku,
            "reserved": stock.reserved,
            "available": stock.available,
            "status": "reserved",
        }

    @app.post("/v1/stock/release")
    def release(body: schemas.ReleaseIn, db: Session = Depends(get_db)):
        try:
            res = services.release(db, body.reservation_id)
        except services.InventoryError as e:
            raise HTTPException(e.code, str(e)) from e
        return {"reservation_id": res.id, "status": res.status}

    @app.post("/v1/stock/adjust", response_model=schemas.StockOut)
    def adjust(body: schemas.AdjustIn, db: Session = Depends(get_db)):
        try:
            stock = services.adjust(db, body.sku, body.warehouse_code, body.delta, body.reason)
        except services.InventoryError as e:
            raise HTTPException(e.code, str(e)) from e
        return schemas.StockOut(
            sku=stock.sku,
            warehouse_id=stock.warehouse_id,
            quantity=stock.quantity,
            reserved=stock.reserved,
            available=stock.available,
        )

    @app.post("/v1/stock/transfer")
    def transfer(body: schemas.TransferIn, db: Session = Depends(get_db)):
        try:
            src, dst = services.transfer(
                db, body.sku, body.from_warehouse, body.to_warehouse, body.qty
            )
        except services.InventoryError as e:
            raise HTTPException(e.code, str(e)) from e
        return {
            "from": {"warehouse_id": src.warehouse_id, "quantity": src.quantity},
            "to": {"warehouse_id": dst.warehouse_id, "quantity": dst.quantity},
        }

    @app.get("/v1/reservations", response_model=list[schemas.ReservationOut])
    def list_res(db: Session = Depends(get_db)):
        return db.scalars(select(models.Reservation).limit(500)).all()

    @app.get("/v1/movements", response_model=list[schemas.MovementOut])
    def list_mov(db: Session = Depends(get_db)):
        return db.scalars(
            select(models.StockMovement).order_by(models.StockMovement.created_at.desc()).limit(500)
        ).all()

    @app.get("/v1/suppliers", response_model=list[schemas.SupplierOut])
    def list_sup(db: Session = Depends(get_db)):
        return db.scalars(select(models.Supplier)).all()

    @app.post("/v1/suppliers", response_model=schemas.SupplierOut, status_code=201)
    def create_sup(body: schemas.SupplierCreate, db: Session = Depends(get_db)):
        row = models.Supplier(**body.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @app.get("/v1/categories", response_model=list[schemas.CategoryOut])
    def list_cat(db: Session = Depends(get_db)):
        return db.scalars(select(models.Category)).all()

    @app.post("/v1/seed")
    def seed(db: Session = Depends(get_db)):
        return seed_demo(db)

    @app.get("/v1/telemetry")
    def telemetry():
        return telemetry_status()

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    # backward-compatible aliases used by orders client
    @app.get("/stock/{sku}")
    def legacy_stock(sku: str, db: Session = Depends(get_db)):
        rows = db.scalars(select(models.StockLevel).where(models.StockLevel.sku == sku)).all()
        if not rows:
            return {"error": "not_found", "sku": sku}
        total_q = sum(r.quantity for r in rows)
        total_r = sum(r.reserved for r in rows)
        return {
            "sku": sku,
            "quantity": total_q,
            "reserved": total_r,
            "available": total_q - total_r,
        }

    @app.post("/reserve")
    def legacy_reserve(body: schemas.ReserveIn, db: Session = Depends(get_db)):
        try:
            res, stock = services.reserve(
                db, body.sku, body.qty, body.warehouse_code, body.order_ref
            )
        except services.InventoryError as e:
            raise HTTPException(e.code, str(e)) from e
        return {
            "sku": stock.sku,
            "reserved": stock.reserved,
            "available": stock.available,
            "status": "reserved",
            "reservation_id": res.id,
        }

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", str(settings.port))),
        reload=False,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
