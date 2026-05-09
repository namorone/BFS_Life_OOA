# CD Pipeline

This document describes the Continuous Deployment setup for **BFS Life — Home Inventory System**.

The repository already has CI in `.github/workflows/ci.yml`. CI is responsible for linting, tests, coverage and frontend build checks. CD is implemented separately in `.github/workflows/cd.yml` and is responsible for Docker image publishing and deployment automation.

---

## Goals

The CD pipeline covers the following tasks:

- build Docker images for backend and frontend;
- push Docker images to GitHub Container Registry (GHCR);
- deploy staging automatically on push;
- deploy production from version tags;
- use versioned Docker tags: `staging`, `latest`, `vX.Y.Z`;
- document deployment requirements and release flow.

---

## Workflow file

Main CD workflow:

```text
.github/workflows/cd.yml
```

It runs on:

```text
push to dev       -> staging images and optional staging deploy
git tag vX.Y.Z    -> production images and optional production deploy
workflow_dispatch -> manual run from GitHub Actions UI
```

---

## Docker images

The project publishes two images:

```text
ghcr.io/<owner>/bfs-life-backend
ghcr.io/<owner>/bfs-life-frontend
```

For this repository, expected image names are:

```text
ghcr.io/namorone/bfs-life-backend
ghcr.io/namorone/bfs-life-frontend
```

---

## Versioning rules

### Staging

Triggered by push to `dev`.

Published tags:

```text
ghcr.io/namorone/bfs-life-backend:staging
ghcr.io/namorone/bfs-life-backend:staging-<short-sha>
ghcr.io/namorone/bfs-life-frontend:staging
ghcr.io/namorone/bfs-life-frontend:staging-<short-sha>
```

### Production

Triggered by a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Published tags:

```text
ghcr.io/namorone/bfs-life-backend:v1.0.0
ghcr.io/namorone/bfs-life-backend:latest
ghcr.io/namorone/bfs-life-frontend:v1.0.0
ghcr.io/namorone/bfs-life-frontend:latest
```

The repository already uses SemVer in the root `VERSION` file and release helpers in the Makefile:

```bash
make release-patch
make release-minor
make release-major
```

After creating a release commit/tag, push both commits and tags:

```bash
git push origin dev
git push origin --tags
```

---

## Deployment strategy

Deployment is SSH-based:

```text
GitHub Actions -> SSH server -> docker compose pull -> docker compose up -d
```

CD uses these compose files:

```text
infra/docker/docker-compose.staging.yml
infra/docker/docker-compose.production.yml
```

Unlike local development compose, these files do not build source code locally. They pull already built images from GHCR.

---

## Required GitHub settings

### Actions permissions

Repository settings:

```text
Settings -> Actions -> General -> Workflow permissions -> Read and write permissions
```

This is required so `GITHUB_TOKEN` can publish packages to GHCR.

### Repository variables

Deployment jobs are disabled by default. Enable them explicitly with repository variables:

```text
ENABLE_STAGING_DEPLOY=true
ENABLE_PRODUCTION_DEPLOY=true
```

Optional server directory variables:

```text
STAGING_APP_DIR=~/BFS_Life_OOA
PRODUCTION_APP_DIR=~/BFS_Life_OOA
```

If these variables are not set, the CD workflow still builds and pushes images, but SSH deployment jobs are skipped.

### Repository secrets

For staging:

```text
STAGING_HOST
STAGING_USER
STAGING_SSH_KEY
```

For production:

```text
PRODUCTION_HOST
PRODUCTION_USER
PRODUCTION_SSH_KEY
```

The SSH key should be a private key with access to the deployment server.

---

## Server requirements

The deployment server must have:

- Docker;
- Docker Compose plugin;
- access to GHCR images;
- repository files or at least `infra/docker/docker-compose.staging.yml` / `infra/docker/docker-compose.production.yml`;
- environment file based on `.env.cd.example`.

Example server setup:

```bash
git clone https://github.com/namorone/BFS_Life_OOA.git
cd BFS_Life_OOA
cp .env.cd.example .env
```

Adjust `.env` values for the target environment.

If GHCR images are private, log in on the server:

```bash
echo <GHCR_TOKEN> | docker login ghcr.io -u <GITHUB_USERNAME> --password-stdin
```

---

## Staging deployment

Triggered automatically by push to `dev` when `ENABLE_STAGING_DEPLOY=true`.

Manual server command equivalent:

```bash
export BACKEND_IMAGE=ghcr.io/namorone/bfs-life-backend:staging
export FRONTEND_IMAGE=ghcr.io/namorone/bfs-life-frontend:staging
docker compose -f infra/docker/docker-compose.staging.yml pull
docker compose -f infra/docker/docker-compose.staging.yml up -d --remove-orphans
```

---

## Production deployment

Triggered automatically by pushing a tag matching `v*.*.*` when `ENABLE_PRODUCTION_DEPLOY=true`.

Manual server command equivalent:

```bash
export BACKEND_IMAGE=ghcr.io/namorone/bfs-life-backend:v1.0.0
export FRONTEND_IMAGE=ghcr.io/namorone/bfs-life-frontend:v1.0.0
docker compose -f infra/docker/docker-compose.production.yml pull
docker compose -f infra/docker/docker-compose.production.yml up -d --remove-orphans
```

---

## Testing CD on a feature branch

Recommended safe workflow:

```bash
git checkout -b feature/cd-pipeline
git add .
git commit -m "Add CD pipeline"
git push origin feature/cd-pipeline
```

By default, CD publishes images only on `dev` and version tags. To test full push behavior on a feature branch, temporarily add the branch to `.github/workflows/cd.yml`:

```yaml
on:
  push:
    branches:
      - dev
      - feature/cd-pipeline
```

Remove the temporary branch trigger before merging to `dev`.

---

## Notes

- Local development continues to use `infra/docker/docker-compose.yml`.
- Staging and production compose files use prebuilt GHCR images.
- Backend containers run `alembic upgrade head` before starting the API.
- Frontend production image uses Nginx and proxies `/api/` and `/media/` to the backend service.
