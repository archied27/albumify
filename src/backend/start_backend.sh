#!/usr/bin/env bash

trap "kill 0" EXIT

echo "Starting Albumify Backend..."
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &

wait