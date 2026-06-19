#!/bin/bash
set -e

ENV_FILE=./server/.env.prod

if [ ! -f "$ENV_FILE" ]; then
  echo "缺少 $ENV_FILE，请先执行: cp server/.env.prod.example server/.env.prod" >&2
  exit 1
fi

docker compose --env-file "$ENV_FILE" -p documents_center up -d --build --force-recreate
