from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app import models


class InventoryError(Exception):
    def __init__(self, message: str, code: int = 400) -> None:
        self.code = code
        super().__init__(message)


def get_warehouse_by_code(db: Session, code: str) -> models.Warehouse:
    wh = db.scalar(select(models.Warehouse).where(models.Warehouse.code == code))
    if not wh:
        raise InventoryError(f"unknown warehouse {code}", 404)
    return wh


def get_or_create_stock(db: Session, sku: str, warehouse_id: str) -> models.StockLevel:
    row = db.scalar(
        select(models.StockLevel).where(
            models.StockLevel.sku == sku,
            models.StockLevel.warehouse_id == warehouse_id,
        )
    )
    if row:
        return row
    row = models.StockLevel(sku=sku, warehouse_id=warehouse_id, quantity=0, reserved=0)
    db.add(row)
    db.flush()
    return row


def reserve(db: Session, sku: str, qty: int, warehouse_code: str | None, order_ref: str | None):
    sku_row = db.get(models.Sku, sku)
    if not sku_row:
        raise InventoryError(f"unknown sku {sku}", 404)
    if warehouse_code:
        wh = get_warehouse_by_code(db, warehouse_code)
    else:
        wh = db.scalars(select(models.Warehouse).limit(1)).first()
        if not wh:
            raise InventoryError("no warehouses", 409)
    stock = get_or_create_stock(db, sku, wh.id)
    if stock.available < qty:
        raise InventoryError("insufficient stock", 409)
    stock.reserved += qty
    res = models.Reservation(
        sku=sku, warehouse_id=wh.id, qty=qty, status="held", order_ref=order_ref
    )
    db.add(res)
    db.add(
        models.StockMovement(
            sku=sku, warehouse_id=wh.id, delta=-qty, reason="reserve", meta=order_ref
        )
    )
    db.commit()
    db.refresh(res)
    db.refresh(stock)
    return res, stock


def release(db: Session, reservation_id: str):
    res = db.get(models.Reservation, reservation_id)
    if not res:
        raise InventoryError("reservation not found", 404)
    if res.status != "held":
        raise InventoryError("reservation not held", 409)
    stock = get_or_create_stock(db, res.sku, res.warehouse_id)
    stock.reserved = max(0, stock.reserved - res.qty)
    res.status = "released"
    db.add(
        models.StockMovement(
            sku=res.sku,
            warehouse_id=res.warehouse_id,
            delta=res.qty,
            reason="release",
            meta=reservation_id,
        )
    )
    db.commit()
    return res


def adjust(db: Session, sku: str, warehouse_code: str, delta: int, reason: str):
    if not db.get(models.Sku, sku):
        raise InventoryError(f"unknown sku {sku}", 404)
    wh = get_warehouse_by_code(db, warehouse_code)
    stock = get_or_create_stock(db, sku, wh.id)
    new_q = stock.quantity + delta
    if new_q < 0 or new_q < stock.reserved:
        raise InventoryError("adjust would make stock inconsistent", 409)
    stock.quantity = new_q
    db.add(models.StockMovement(sku=sku, warehouse_id=wh.id, delta=delta, reason=reason))
    db.commit()
    db.refresh(stock)
    return stock


def transfer(db: Session, sku: str, from_code: str, to_code: str, qty: int):
    if qty <= 0:
        raise InventoryError("qty must be > 0")
    if not db.get(models.Sku, sku):
        raise InventoryError(f"unknown sku {sku}", 404)
    src = get_warehouse_by_code(db, from_code)
    dst = get_warehouse_by_code(db, to_code)
    if src.id == dst.id:
        raise InventoryError("same warehouse", 400)
    s_stock = get_or_create_stock(db, sku, src.id)
    if s_stock.available < qty:
        raise InventoryError("insufficient stock for transfer", 409)
    s_stock.quantity -= qty
    d_stock = get_or_create_stock(db, sku, dst.id)
    d_stock.quantity += qty
    db.add(models.StockMovement(sku=sku, warehouse_id=src.id, delta=-qty, reason="transfer_out"))
    db.add(models.StockMovement(sku=sku, warehouse_id=dst.id, delta=qty, reason="transfer_in"))
    db.commit()
    return s_stock, d_stock
