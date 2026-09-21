from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SkuCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str
    category_id: str | None = None
    supplier_id: str | None = None
    unit_cost_cents: int = 0


class SkuUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    unit_cost_cents: int | None = None


class SkuOut(BaseModel):
    sku: str
    name: str
    status: str
    unit_cost_cents: int

    model_config = {"from_attributes": True}


class WarehouseCreate(BaseModel):
    code: str
    name: str
    region: str = "US"


class WarehouseOut(BaseModel):
    id: str
    code: str
    name: str
    region: str
    model_config = {"from_attributes": True}


class SupplierCreate(BaseModel):
    code: str
    name: str
    email: str | None = None
    phone: str | None = None


class SupplierOut(BaseModel):
    id: str
    code: str
    name: str
    model_config = {"from_attributes": True}


class StockOut(BaseModel):
    sku: str
    warehouse_id: str
    quantity: int
    reserved: int
    available: int


class ReserveIn(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    warehouse_code: str | None = None
    order_ref: str | None = None


class ReleaseIn(BaseModel):
    reservation_id: str


class AdjustIn(BaseModel):
    sku: str
    warehouse_code: str
    delta: int
    reason: str = "manual_adjust"


class TransferIn(BaseModel):
    sku: str
    from_warehouse: str
    to_warehouse: str
    qty: int = Field(gt=0)


class ReservationOut(BaseModel):
    id: str
    sku: str
    warehouse_id: str
    qty: int
    status: str
    order_ref: str | None
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class MovementOut(BaseModel):
    id: str
    sku: str
    warehouse_id: str
    delta: int
    reason: str
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: str
    name: str
    model_config = {"from_attributes": True}
