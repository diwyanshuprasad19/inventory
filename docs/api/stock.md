# Inventory — stock, reservations, movements

Schemas: `ReserveIn`, `ReleaseIn`, `AdjustIn`, `TransferIn`, `StockOut`, … · Service: `inventory_app.services` · Routes: `src/inventory_app/app.py`

## List stock

`GET /v1/stock` · `list_stock` · limit 1000 · response `list[StockOut]`

| Field | Type | Description |
|-------|------|-------------|
| sku | string | SKU |
| warehouse_id | string | Warehouse UUID |
| quantity | integer | On-hand |
| reserved | integer | Reserved |
| available | integer | `quantity - reserved` (via property) |

---

## Stock by SKU

`GET /v1/stock/{sku}` · `stock_sku` · **404** if no rows · else `list[StockOut]`.

---

## Reserve stock

**Purpose:** Hold quantity for an order (increments `reserved`, creates `Reservation` + `StockMovement`).

| | |
|--|--|
| Method | `POST` |
| URL | `/v1/stock/reserve` |
| Handler | `reserve` |
| Service | `services.reserve` |
| Request | `ReserveIn` |

**ReserveIn**

| Field | Type | Required | Nullable | Default | Validation | Description |
|-------|------|----------|----------|---------|------------|-------------|
| sku | string | Yes | No | — | — | SKU |
| qty | integer | Yes | No | — | `gt=0` | Quantity |
| warehouse_code | string | No | Yes | null | — | Defaults to first warehouse if omitted |
| order_ref | string | No | Yes | null | — | Optional reference |

**Sample:**
```json
{"sku":"WIDGET-1","qty":2,"warehouse_code":"WH-EAST","order_ref":"ord-demo"}
```

**Success `200`:**
```json
{
  "reservation_id": "<uuid>",
  "sku": "WIDGET-1",
  "reserved": 2,
  "available": 98,
  "status": "reserved"
}
```

**Errors (HTTPException from `InventoryError.code`)**

| Status | Typical message |
|--------|-----------------|
| 404 | unknown sku / unknown warehouse |
| 409 | insufficient stock / no warehouses |
| 422 | qty ≤ 0 or invalid body |

**DB:** Updates `StockLevel.reserved`; creates `Reservation` (`status=held`); creates `StockMovement` (`reason=reserve`).

**Internal flow:** Router → `reserve` → `services.reserve` → commit → JSON.

---

## Release reservation

`POST /v1/stock/release` · body `ReleaseIn` `{ "reservation_id": "<uuid>" }` · `services.release`

**Success `200`:** `{"reservation_id","status"}` with status `released`.  
Idempotent if already `released` (cancel/retry). **409** if status is `consumed` or other non-held.

Locks reservation + stock rows (`FOR UPDATE`).

---

## Consume reservation (fulfill / ship)

`POST /v1/stock/consume` · body `ReleaseIn` · `services.consume`

Finalizes a held reservation: decrements `quantity` and `reserved`, status → `consumed`.  
Idempotent if already `consumed`. Legacy alias: `POST /consume`.

**Errors:** 404 missing · 409 not held / stock inconsistent

---**404** reservation not found · **409** reservation not `held`.

---

## Adjust stock

`POST /v1/stock/adjust` · `AdjustIn` · response `StockOut`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| sku | string | Yes | — | SKU |
| warehouse_code | string | Yes | — | Warehouse code |
| delta | integer | Yes | — | Signed delta |
| reason | string | No | `manual_adjust` | Reason |

**409** if resulting quantity &lt; 0 or &lt; reserved · **404** unknown sku/warehouse.

---

## Transfer

`POST /v1/stock/transfer` · `TransferIn`

| Field | Required | Validation |
|-------|----------|------------|
| sku | Yes | must exist |
| from_warehouse | Yes | code |
| to_warehouse | Yes | code |
| qty | Yes | `gt=0` |

**400** same warehouse · **404** unknown sku/warehouse · **409** insufficient available.

**Success:** `{"from":{"warehouse_id","quantity"},"to":{"warehouse_id","quantity"}}`.

---

## List reservations / movements

- `GET /v1/reservations` → `list[ReservationOut]` limit 500  
- `GET /v1/movements` → `list[MovementOut]` newest first limit 500  

**ReservationOut:** id, sku, warehouse_id, qty, status, order_ref, created_at  
**MovementOut:** id, sku, warehouse_id, delta, reason, created_at
