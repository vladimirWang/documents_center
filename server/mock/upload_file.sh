#!/bin/zsh

SCRIPT_DIR="${0:A:h}"
TEST_FILE="${SCRIPT_DIR}/test_upload.txt"

echo "hello upload" > "$TEST_FILE"

resp=$(curl -sS -X POST http://localhost:8000/file/upload \
  -F "file=@${TEST_FILE}")

echo "resp is $resp"
