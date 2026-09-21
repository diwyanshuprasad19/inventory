# Inventory — warehouses

## List warehouses

`GET /v1/warehouses` · `list_wh` · response `list[WarehouseOut]`

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID |
| code | string | Unique code |
| name | string | Name |
| region | string | Region |

## Create warehouse

`POST /v1/warehouses` · `201` · `WarehouseCreate`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| code | string | Yes | — | Unique code |
| name | string | Yes | — | Name |
| region | string | No | `"US"` | Region |

Handler: `create_wh` · Model: `Warehouse` · File: `src/inventory_app/app.py`
