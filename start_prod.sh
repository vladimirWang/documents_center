#!/bin/bash
#
docker compose --env-file ./server/.env.prod -p documents_center up -d --build
