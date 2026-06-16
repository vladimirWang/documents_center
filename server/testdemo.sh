#!/bin/bash

resp=$(curl -sS -X GET http://localhost:8000/chat/sessions)

echo "resp: $resp"