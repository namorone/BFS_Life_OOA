#!/bin/bash

set -e

ENVIRONMENT=${1:-production}
BACKEND_TAG=${2}
FRONTEND_TAG=${3:-$BACKEND_TAG}

if [ -z "$BACKEND_TAG" ]; then
  echo "Usage:"
  echo "./infra/deploy/rollback.sh production v1.0.0"
  echo "./infra/deploy/rollback.sh staging staging"
  exit 1
fi

COMPOSE_FILE="infra/docker/docker-compose.${ENVIRONMENT}.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "Compose file not found: $COMPOSE_FILE"
  exit 1
fi

echo "Rolling back $ENVIRONMENT environment"
echo "Backend image tag: $BACKEND_TAG"
echo "Frontend image tag: $FRONTEND_TAG"

export BACKEND_IMAGE="ghcr.io/OWNER/REPO/backend:${BACKEND_TAG}"
export FRONTEND_IMAGE="ghcr.io/OWNER/REPO/frontend:${FRONTEND_TAG}"

docker compose -f "$COMPOSE_FILE" pull
docker compose -f "$COMPOSE_FILE" up -d

echo "Rollback completed."
