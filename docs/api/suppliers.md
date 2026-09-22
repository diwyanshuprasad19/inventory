# Inventory — suppliers

## List

`GET /v1/suppliers` · `list_sup` · `list[SupplierOut]` (`id`, `code`, `name`)

## Create

`POST /v1/suppliers` · `201` · `SupplierCreate`

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| code | string | Yes | No | Unique code |
| name | string | Yes | No | Name |
| email | string | No | Yes | Email |
| phone | string | No | Yes | Phone |

Handler: `create_sup` · Model: `Supplier`
