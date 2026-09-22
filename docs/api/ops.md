# Inventory — ops / health / seed / telemetry

## Health

**Purpose:** Process liveness probe.

| | |
|--|--|
| Method | `GET` |
| URL | `/health` |
| Handler | `inventory_app.app.create_app.<locals>.health` |
| File | `src/inventory_app/app.py` |

**Auth:** Not explicitly enforced.

**Success:** `200` · `{"status":"ok","service":"inventory"}`

---

## Ready

**Purpose:** Readiness including database connectivity (`SELECT 1`).

| | |
|--|--|
| Method | `GET` |
| URL | `/ready` |
| Handler | `ready` |
| File | `src/inventory_app/app.py` |
| DB | `get_db` → SQLAlchemy session |

**Auth:** Not explicitly enforced.

**Success:** `200` · `{"status":"ready"}`  
**Failure:** If DB is down, FastAPI/SQLAlchemy will raise (typically `500`) — not a custom JSON error shape in handler.

---

## Metrics

**Purpose:** Prometheus metrics exposition.

| | |
|--|--|
| Method | `GET` |
| URL | `/metrics` |
| Handler | `metrics` |
| File | `src/inventory_app/app.py` |
| Library | `prometheus_client.generate_latest` |

**Success:** `200` · `Content-Type` from `CONTENT_TYPE_LATEST` (Prometheus text).

---

## Telemetry status

**Purpose:** Report whether OpenTelemetry tracer provider is configured.

| | |
|--|--|
| Method | `GET` |
| URL | `/v1/telemetry` |
| Handler | `telemetry` |
| File | `src/inventory_app/app.py` |
| Helper | `distributed_tracing.health_telemetry.telemetry_status` (when importable) |

**Success:** `200` · JSON keys include `tracing_configured`, `provider`, `meter_provider`, `otlp_endpoint`, `service_name`, `sampler_arg` (from helper).

**Security:** Do not put secrets in this response; current helper exposes endpoint URL from env name defaults only.

---

## Seed demo data

**Purpose:** Insert demo category, supplier, warehouses, SKUs, and stock if missing.

| | |
|--|--|
| Method | `POST` |
| URL | `/v1/seed` |
| Handler | `seed` |
| File | `src/inventory_app/app.py` |
| Service | `inventory_app.seed.seed_demo` |

**Request body:** none required.

**Success:** `200` · e.g. `{"skus_created": <int>, "warehouses": <int>, "category": "Electronics"}` (values depend on prior DB state).

**Database effects:** May create `Category`, `Supplier`, `Warehouse`, `Sku`, `StockLevel` rows (idempotent-ish: skips existing codes/skus).
