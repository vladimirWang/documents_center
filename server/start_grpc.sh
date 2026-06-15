#!/bin/bash
set -e

cd "$(dirname "$0")"

cleanup() {
  if [ -n "${WATCHER_PID:-}" ]; then
    kill "$WATCHER_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "starting proto watcher..."
uv run python scripts/watch_grpc.py &
WATCHER_PID=$!

uv run python -m grpc_server.server
