# Inventory microservice

Stock check + reserve API with distributed tracing (OTLP → Alloy).

```bash
pip install -e ".[dev]"
# sibling tracing lib
pip install -e ../distributed-tracing
pytest tests/ -q
PORT=8091 python -m inventory_app.app
# GET http://localhost:8091/health
# GET http://localhost:8091/stock/sku-100
```

Local-first: `make -C ../platform-ops local-gate REPO=inventory`
