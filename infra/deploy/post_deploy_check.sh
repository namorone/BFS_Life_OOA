#!/bin/bash

set -e

BACKEND_URL=${1:-http://localhost:8000}

echo "Running post-deploy healthcheck..."
echo "Backend URL: $BACKEND_URL"

curl -fsS "$BACKEND_URL/api/v1/health"

echo ""
echo "Post-deploy check passed successfully."
