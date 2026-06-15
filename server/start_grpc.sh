#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

cleanup() {
  if [ -n "${WATCHER_PID:-}" ]; then
    kill "$WATCHER_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "generating gRPC stubs..."
bash scripts/generate_grpc.sh

echo "starting proto watcher..."
uv run python scripts/watch_grpc.py --watch-only &
WATCHER_PID=$!

uv run python -m grpc_server.server
