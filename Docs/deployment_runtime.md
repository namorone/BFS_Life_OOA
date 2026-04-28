# Deployment & Runtime Infrastructure

## 1. Purpose

This document describes the runtime infrastructure for the BFS Life project, including staging and production environments, deployment strategy, health checks, monitoring and rollback process.

---

## 2. Environments

The project uses two runtime environments:

| Environment | Purpose | Compose file |
|------------|---------|--------------|
| Staging | Testing new changes before production | `infra/docker/docker-compose.staging.yml` |
| Production | Stable user-facing environment | `infra/docker/docker-compose.production.yml` |

---

## 3. Staging Environment

The staging environment is used to verify new versions before release.

Default ports:

| Service | Port |
|--------|------|
| Frontend | `3001` |
| Backend | `8001` |
| PostgreSQL | `5434` |

Run staging:

```bash
docker compose -f infra/docker/docker-compose.staging.yml up -d
