#!/bin/bash
# Pterodactyl startup script for AI Inference
set -e

# Start inference service
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
