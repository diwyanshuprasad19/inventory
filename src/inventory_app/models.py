from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory_app.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str | None] = mapped_column(String(256))
    phone: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Warehouse(Base):
    __tablename__ = "warehouses"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    region: Mapped[str] = mapped_column(String(64), default="US", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    stocks: Mapped[list[StockLevel]] = relationship(back_populates="warehouse")


class Sku(Base):
    __tablename__ = "skus"
    sku: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    category_id: Mapped[str | None] = mapped_column(ForeignKey("categories.id"), index=True)
    supplier_id: Mapped[str | None] = mapped_column(ForeignKey("suppliers.id"), index=True)
    unit_cost_cents: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    stocks: Mapped[list[StockLevel]] = relationship(back_populates="sku_row")


class StockLevel(Base):
    __tablename__ = "stock_levels"
    __table_args__ = (UniqueConstraint("sku", "warehouse_id", name="uq_stock_sku_wh"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    sku: Mapped[str] = mapped_column(ForeignKey("skus.sku"), nullable=False, index=True)
    warehouse_id: Mapped[str] = mapped_column(ForeignKey("warehouses.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved: Mapped[int] = mapped_column(Integer, default=0)
    sku_row: Mapped[Sku] = relationship(back_populates="stocks")
    warehouse: Mapped[Warehouse] = relationship(back_populates="stocks")

    @property
    def available(self) -> int:
        return max(0, self.quantity - self.reserved)


class Reservation(Base):
    __tablename__ = "reservations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    sku: Mapped[str] = mapped_column(ForeignKey("skus.sku"), nullable=False, index=True)
    warehouse_id: Mapped[str] = mapped_column(ForeignKey("warehouses.id"), nullable=False, index=True)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="held", index=True)
    order_ref: Mapped[str | None] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class StockMovement(Base):
    __tablename__ = "stock_movements"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    sku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    warehouse_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    meta: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
