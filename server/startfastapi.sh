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
  if [ -n "${GRPC_PID:-}" ]; then
    kill "$GRPC_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "generating gRPC stubs..."
bash scripts/generate_grpc.sh

echo "starting proto watcher..."
uv run python scripts/watch_grpc.py --watch-only &
WATCHER_PID=$!

echo "starting gRPC server..."
uv run python -m grpc_server.server &
GRPC_PID=$!

sleep 1
if ! kill -0 "$GRPC_PID" 2>/dev/null; then
  echo "gRPC server failed to start" >&2
  exit 1
fi

echo "starting FastAPI..."
uv run python main.py
