# Inventory — categories

## List categories

`GET /v1/categories` · `list_cat` · `list[CategoryOut]`

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID |
| name | string | Unique name |

**Note:** There is no `POST /v1/categories` in `app.py`; categories are created via seed / DB. Do not invent a create endpoint.
