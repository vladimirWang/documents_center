#!/bin/bash
set -e
cd "$(dirname "$0")"

bash scripts/generate_grpc.sh
uv run --env-file .env.dev python main.py