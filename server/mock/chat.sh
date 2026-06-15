#!/bin/bash

resp=$(curl -s -X POST http://localhost:8000/chat/ \
-d '{"question": "你好", "session_id": "123"}' \
-H "Content-Type: application/json")

echo "resp is $resp"