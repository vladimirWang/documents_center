#!/bin/bash
set -e

DB_HOST="${DB_HOST:-postgres}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
DB_NAME="${DB_NAME:-documents_center}"

echo "ensuring database ${DB_NAME} exists..."
uv run python - <<PY
import psycopg

conn = psycopg.connect(
    host="${DB_HOST}",
    user="${DB_USER}",
    password="${DB_PASSWORD}",
    dbname="postgres",
)
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", ("${DB_NAME}",))
    if cur.fetchone() is None:
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
conn.close()
PY

echo "running alembic migrations..."
uv run alembic upgrade head

exec uv run "$@"
