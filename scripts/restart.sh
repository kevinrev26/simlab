#!/bin/bash
set -e

echo "====> Shutting down"
docker compose -f dev.compose.yml down
echo "====> Starting the infra"
docker compose -f dev.compose.yml up --build -d