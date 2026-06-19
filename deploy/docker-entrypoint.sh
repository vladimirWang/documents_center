#!/bin/bash
set -e


echo "running alembic migrations..."
uv run alembic upgrade head

exec uv run "$@"
