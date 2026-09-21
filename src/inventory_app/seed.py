from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app import models

DEMO_SKUS = [
    ("WIDGET-1", "Blue Widget", 100, 1200),
    ("WIDGET-2", "Red Widget", 50, 1500),
    ("GADGET-9", "Pro Gadget", 25, 9900),
    ("CABLE-USB-C", "USB-C Cable 2m", 500, 799),
    ("BATTERY-AA", "AA Battery 4-pack", 1000, 499),
    ("CASE-PHONE", "Phone Case Clear", 200, 1299),
    ("CHARGER-20W", "20W Charger", 150, 2499),
    ("HUB-USB", "USB Hub 7-port", 80, 3499),
    ("MOUSE-WL", "Wireless Mouse", 120, 2199),
    ("KB-MECH", "Mechanical Keyboard", 60, 8999),
    ("MONITOR-27", "27in Monitor", 40, 24999),
    ("SSD-1TB", "1TB NVMe SSD", 90, 7999),
]


def seed_demo(db: Session) -> dict:
    cat = db.scalar(select(models.Category).where(models.Category.name == "Electronics"))
    if not cat:
        cat = models.Category(name="Electronics", description="Consumer electronics")
        db.add(cat)
        db.flush()

    sup = db.scalar(select(models.Supplier).where(models.Supplier.code == "ACME"))
    if not sup:
        sup = models.Supplier(code="ACME", name="Acme Supply Co", email="ops@acme.example")
        db.add(sup)
        db.flush()

    warehouses = []
    for code, name, region in [
        ("WH-EAST", "East Coast DC", "US-E"),
        ("WH-WEST", "West Coast DC", "US-W"),
        ("WH-EU", "EU Hub", "EU"),
    ]:
        wh = db.scalar(select(models.Warehouse).where(models.Warehouse.code == code))
        if not wh:
            wh = models.Warehouse(code=code, name=name, region=region)
            db.add(wh)
            db.flush()
        warehouses.append(wh)

    created = 0
    for sku, name, qty, cost in DEMO_SKUS:
        row = db.get(models.Sku, sku)
        if not row:
            row = models.Sku(
                sku=sku,
                name=name,
                category_id=cat.id,
                supplier_id=sup.id,
                unit_cost_cents=cost,
            )
            db.add(row)
            db.flush()
            created += 1
        # put stock in east warehouse
        stock = db.scalar(
            select(models.StockLevel).where(
                models.StockLevel.sku == sku,
                models.StockLevel.warehouse_id == warehouses[0].id,
            )
        )
        if not stock:
            db.add(
                models.StockLevel(
                    sku=sku,
                    warehouse_id=warehouses[0].id,
                    quantity=qty,
                    reserved=0,
                )
            )
    db.commit()
    return {"skus_created": created, "warehouses": len(warehouses), "category": cat.name}
