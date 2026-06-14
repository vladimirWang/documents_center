#!/bin/bash

uv run streamlit run main.py \
  --server.runOnSave=true \
  --server.fileWatcherType=poll
