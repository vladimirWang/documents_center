#!/usr/bin/env python3
"""监听 server/protos 目录，proto 变更时自动执行 generate_grpc.sh。"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTOS_DIR = ROOT / "protos"
GENERATE_SCRIPT = ROOT / "scripts" / "generate_grpc.sh"
POLL_INTERVAL_SEC = 1.0


def proto_fingerprint() -> str:
    digest = hashlib.md5()
    for proto_file in sorted(PROTOS_DIR.glob("*.proto")):
        digest.update(proto_file.name.encode())
        digest.update(proto_file.read_bytes())
    return digest.hexdigest()


def run_generate() -> None:
    print("[watch_grpc] generating stubs...")
    subprocess.run(["bash", str(GENERATE_SCRIPT)], cwd=ROOT, check=True)


def main() -> int:
    if not PROTOS_DIR.exists():
        print(f"[watch_grpc] protos directory not found: {PROTOS_DIR}", file=sys.stderr)
        return 1

    proto_files = list(PROTOS_DIR.glob("*.proto"))
    if not proto_files:
        print(f"[watch_grpc] no .proto files in {PROTOS_DIR}", file=sys.stderr)
        return 1

    run_generate()
    last_fingerprint = proto_fingerprint()
    print(f"[watch_grpc] watching {PROTOS_DIR} ({len(proto_files)} file(s))")

    while True:
        time.sleep(POLL_INTERVAL_SEC)
        current = proto_fingerprint()
        if current == last_fingerprint:
            continue
        last_fingerprint = current
        try:
            run_generate()
            print("[watch_grpc] stubs updated")
        except subprocess.CalledProcessError:
            print("[watch_grpc] generation failed, waiting for next change", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
