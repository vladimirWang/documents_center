#!/bin/zsh
resp=$(curl -sS -X GET http://localhost:8000/response)

echo "resp is $resp"
