#!/bin/bash
set -e

cd "$(dirname "$0")"

uv sync
uv run streamlit run app.py \
  --server.runOnSave=true \
  --server.fileWatcherType=poll \
  --server.port=8501
