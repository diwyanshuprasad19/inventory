# inventory

Production inventory microservice (FastAPI + Postgres/Alembic + OpenTelemetry).

## APIs (≥20)
- `GET /health` — liveness\n- `GET /ready` — readiness + db\n- `GET /v1/skus` — list SKUs\n- `POST /v1/skus` — create SKU\n- `GET /v1/skus/{sku}` — get SKU\n- `PATCH /v1/skus/{sku}` — update SKU\n- `GET /v1/warehouses` — list warehouses\n- `POST /v1/warehouses` — create warehouse\n- `GET /v1/stock` — list stock levels\n- `GET /v1/stock/{sku}` — stock by SKU\n- `POST /v1/stock/reserve` — reserve stock\n- `POST /v1/stock/release` — release reservation\n- `POST /v1/stock/adjust` — adjust quantity\n- `POST /v1/stock/transfer` — transfer between warehouses\n- `GET /v1/reservations` — list reservations\n- `GET /v1/movements` — stock movement ledger\n- `GET /v1/suppliers` — list suppliers\n- `POST /v1/suppliers` — create supplier\n- `GET /v1/categories` — list categories\n- `POST /v1/seed` — seed demo data\n- `GET /v1/telemetry` — otel status\n- `GET /metrics` — prometheus text

```bash
pip install -e ".[dev]"
# also: pip install -e ../distributed-tracing
alembic upgrade head
PORT=8091 python -m inventory_app.app
curl -X POST localhost:8091/v1/seed
```
