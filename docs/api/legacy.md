# Inventory — legacy aliases (orders client compatibility)

These routes exist for the orders `InventoryClient` (`/stock/{sku}`, `/reserve`). Prefer `/v1/*` for new clients.

## Legacy stock

`GET /stock/{sku}` · `legacy_stock`

**Success `200`:** Aggregates all warehouses:
```json
{"sku":"WIDGET-1","quantity":100,"reserved":0,"available":100}
```

If no stock rows: **still HTTP 200** with `{"error":"not_found","sku":"<sku>"}` (not 404). Documented as implemented.

## Legacy reserve

`POST /reserve` · body `ReserveIn` · same service as `/v1/stock/reserve`

**Success `200`:** includes `reservation_id`, `sku`, `reserved`, `available`, `status`.

## Legacy release

`POST /release` · body `ReleaseIn` · same as `/v1/stock/release`

## Legacy consume

`POST /consume` · body `ReleaseIn` · same as `/v1/stock/consume` (used by orders on ship)
