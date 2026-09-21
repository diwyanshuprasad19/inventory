"""Inventory HTTP API — /health, /stock/<sku>, /reserve."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request

# Prefer sibling distributed-tracing package when present
_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from inventory_app.store import InventoryStore, StockError

try:
    from distributed_tracing import configure_tracing, extract_context, get_tracer
    from opentelemetry.trace import SpanKind
except ImportError:  # pragma: no cover
    configure_tracing = None  # type: ignore
    extract_context = None  # type: ignore
    get_tracer = None  # type: ignore
    SpanKind = None  # type: ignore

STORE = InventoryStore()


def create_app() -> Flask:
    app = Flask(__name__)
    if configure_tracing:
        configure_tracing(os.getenv("OTEL_SERVICE_NAME", "inventory"))

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "inventory"})

    @app.get("/stock/<sku>")
    def stock(sku: str):
        tracer = get_tracer(__name__) if get_tracer else None
        ctx = extract_context(dict(request.headers)) if extract_context else None
        span_cm = (
            tracer.start_as_current_span("inventory.stock", context=ctx, kind=SpanKind.SERVER)
            if tracer
            else None
        )
        try:
            if span_cm:
                span_cm.__enter__()
            item = STORE.get(sku)
            body = {
                "sku": item.sku,
                "quantity": item.quantity,
                "reserved": item.reserved,
                "available": item.available,
            }
            return jsonify(body)
        except StockError as exc:
            return jsonify({"error": str(exc)}), 404
        finally:
            if span_cm:
                span_cm.__exit__(None, None, None)

    @app.post("/reserve")
    def reserve():
        data = request.get_json(silent=True) or {}
        sku = str(data.get("sku", ""))
        qty = int(data.get("qty", 0))
        try:
            item = STORE.reserve(sku, qty)
            return jsonify(
                {
                    "sku": item.sku,
                    "reserved": item.reserved,
                    "available": item.available,
                    "status": "reserved",
                }
            )
        except StockError as exc:
            code = 404 if "unknown" in str(exc) else 409
            return jsonify({"error": str(exc)}), code

    return app


app = create_app()


def main() -> None:
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8091")), debug=False)


if __name__ == "__main__":
    main()
