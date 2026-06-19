#!/bin/bash
set -e

cd "$(dirname "$0")/.."

shopt -s nullglob
proto_files=(./protos/*.proto)
shopt -u nullglob

if [ ${#proto_files[@]} -eq 0 ]; then
  echo "no .proto files found in ./protos"
  exit 1
fi

mkdir -p ./grpc_generated
touch ./grpc_generated/__init__.py

uv run python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./grpc_generated \
  --grpc_python_out=./grpc_generated \
  "${proto_files[@]}"

uv run python - <<'PY'
import re
from pathlib import Path

for grpc_stub in Path("grpc_generated").glob("*_pb2_grpc.py"):
    content = grpc_stub.read_text(encoding="utf-8")
    updated = re.sub(
        r"^import (\w+_pb2) as",
        r"from grpc_generated import \1 as",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    grpc_stub.write_text(updated, encoding="utf-8")

print("gRPC stubs generated.")
PY
