# Inventory — SKUs

Schemas: `src/inventory_app/schemas.py` · Model: `inventory_app.models.Sku` · Routes: `src/inventory_app/app.py`

## List SKUs

**Purpose:** Return up to 500 SKU rows for catalog browsing / clients.

| | |
|--|--|
| Method | `GET` |
| URL | `/v1/skus` |
| Handler | `list_skus` |
| Response model | `list[SkuOut]` |

**Auth:** Not explicitly enforced.

**Success `200` — SkuOut fields**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| sku | string | No | Primary key |
| name | string | No | Display name |
| status | string | No | e.g. default `active` on create |
| unit_cost_cents | integer | No | Cost in cents |

---

## Create SKU

**Purpose:** Create a catalog SKU.

| | |
|--|--|
| Method | `POST` |
| URL | `/v1/skus` |
| Status | `201` on success |
| Handler | `create_sku` |
| Request schema | `SkuCreate` |

**Content-Type:** `application/json`

**Request fields (SkuCreate)**

| Field | Type | Required | Nullable | Default | Validation | Description |
|-------|------|----------|----------|---------|------------|-------------|
| sku | string | Yes | No | — | min 1, max 64 | SKU id |
| name | string | Yes | No | — | — | Name |
| category_id | string | No | Yes | null | — | FK category |
| supplier_id | string | No | Yes | null | — | FK supplier |
| unit_cost_cents | integer | No | No | `0` | — | Cost cents |

**Sample request (synthetic):**
```json
{
  "sku": "NEW-SKU-1",
  "name": "New Item",
  "unit_cost_cents": 500
}
```

**curl:**
```bash
curl --request POST \
  --url '<BASE_URL>/v1/skus' \
  --header 'Content-Type: application/json' \
  --data '{"sku":"NEW-SKU-1","name":"New Item","unit_cost_cents":500}'
```

**Success `201`:** `SkuOut` body.

**Errors**

| Status | When (from code) |
|--------|------------------|
| 409 | `"sku exists"` if SKU already present |
| 422 | Pydantic validation failure |

**Database:** Creates `Sku`.

---

## Get SKU

| | |
|--|--|
| Method | `GET` |
| URL | `/v1/skus/{sku}` |
| Handler | `get_sku` |

**Path:** `sku` string.

**Success `200`:** `SkuOut` · **404** `{"detail":"not found"}` (FastAPI HTTPException detail).

---

## Patch SKU

| | |
|--|--|
| Method | `PATCH` |
| URL | `/v1/skus/{sku}` |
| Handler | `patch_sku` |
| Request schema | `SkuUpdate` |

**SkuUpdate fields** (all optional)

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| name | string | No | Yes | New name |
| status | string | No | Yes | Status |
| unit_cost_cents | integer | No | Yes | Cost |

Only fields sent are applied (`exclude_unset=True`).

**404** if SKU missing · **200** `SkuOut` on success.
