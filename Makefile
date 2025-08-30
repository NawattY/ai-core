.PHONY: db-migrate run api test

db-migrate:
	psql postgresql://postgres:postgres@localhost:5432/ai_core -f scripts/bootstrap_pgvector.sql

run:
	uvicorn src.services.api:app --reload --port 8000

api: run

test:
	pytest -q
