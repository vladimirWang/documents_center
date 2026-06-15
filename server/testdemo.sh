#!/bin/bash

resp=$(curl -sS -X POST http://localhost:8002/ \
-d '{"username":"mike", "mobile":"13800138011"}' \
-H "Content-Type: application/json")

echo "resp: $resp"