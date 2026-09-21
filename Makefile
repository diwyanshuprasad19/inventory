.PHONY: migrate seed run test
migrate:
	alembic upgrade head
seed:
	curl -s -X POST http://127.0.0.1:$${PORT:-8091}/v1/seed | python3 -m json.tool
run:
	PORT=$${PORT:-8091} python -m inventory_app.app
test:
	pytest -q
