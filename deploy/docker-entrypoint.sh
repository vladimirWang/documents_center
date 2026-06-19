#!/bin/bash
set -e

if [ -z "${SQLALCHEMY_DATABASE_URL:-}" ]; then
  echo "ERROR: SQLALCHEMY_DATABASE_URL 未注入容器，请检查 docker-compose.yml 的 env_file / environment" >&2
  exit 1
fi

db_target="${SQLALCHEMY_DATABASE_URL#*@}"
echo "running alembic migrations... (target: ${db_target})"
uv run alembic upgrade head

exec uv run "$@"
