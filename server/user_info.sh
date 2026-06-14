#!/bin/zsh
resp=$(curl -sS -X POST http://localhost:8000/user/login \
-d '{"username":"mike", "password":"123456"}' \
-H "Content-Type: application/json")

token=$(jq -r ".token" <<< "$resp")

info_resp=$(curl -sS http://localhost:8000/user/user_info \
-H "Authorization: Bearer ${token}")
echo "info_resp is $info_resp"
