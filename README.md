# 🏠 BFS Life — Home Inventory System

Fullstack application for managing home inventory, items, categories, and expenses.

---

# 🚀 Tech Stack

* **Backend:** FastAPI (Python)
* **Frontend:** React + Vite
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Containerization:** Docker + Docker Compose
* **Linting:** Ruff (backend), ESLint (frontend)

---

# 🧱 Project Structure

This project follows a **monorepo architecture** with separation of concerns between backend, frontend, and infrastructure.

---

## 📁 Root

```id="root-structure"
BFS_Life_OOA/
├── apps/              # application code
├── infra/             # infrastructure (docker)
├── packages/          # shared code (optional)
├── .env               # environment variables
├── Makefile           # helper commands
├── README.md
```

---

## 🧠 apps/

Contains all main applications.

```id="apps-structure"
apps/
├── backend/
├── frontend/
```

---

# 🖥 Backend (FastAPI)

```id="backend-structure"
apps/backend/
├── app/
│   ├── api/              # API routes
│   │   └── v1/
│   │       ├── routes/   # endpoints (auth, categories, etc.)
│   │       └── router.py
│   │
│   ├── core/             # config, security, settings
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py       # Base model
│   │   ├── session.py    # DB session
│   │   └── models/       # SQLAlchemy models
│   │       ├── user.py
│   │       └── category.py
│   │
│   ├── schemas/          # Pydantic schemas
│   │   ├── user.py
│   │   └── category.py
│   │
│   ├── services/         # business logic
│   ├── repositories/     # DB access layer
│   │
│   ├── main.py           # app entrypoint
│   │
│   └── __init__.py
│
├── alembic/              # migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/                # backend tests
│
├── pyproject.toml        # dependencies (poetry)
├── alembic.ini           # alembic config
├── Dockerfile
```

---

## 🧠 Backend Layers

| Layer        | Responsibility              |
| ------------ | --------------------------- |
| API          | HTTP endpoints              |
| Schemas      | request/response validation |
| Services     | business logic              |
| Repositories | DB queries                  |
| Models       | DB structure                |

---

# 🌐 Frontend (React + Vite)

```id="frontend-structure"
apps/frontend/
├── src/
│   ├── app/              # app setup (router, providers)
│   │   ├── App.jsx
│   │   └── router.jsx
│   │
│   ├── pages/            # pages (Login, Dashboard, etc.)
│   │
│   ├── features/         # business logic (auth, categories)
│   │
│   ├── components/       # reusable UI components
│   │
│   ├── services/         # API calls
│   │
│   ├── hooks/            # custom hooks
│   │
│   ├── shared/           # utils, constants
│   │
│   ├── styles/           # global styles
│   │
│   └── main.jsx
│
├── public/
├── package.json
├── Dockerfile
```

---

## 🧠 Frontend Layers

| Layer      | Responsibility   |
| ---------- | ---------------- |
| pages      | UI screens       |
| components | reusable UI      |
| features   | logic per domain |
| services   | API calls        |
| hooks      | reusable logic   |



# 🔄 Data Flow

```id="flow"
Frontend → API → Service → Repository → Database
```

---

# 📌 Key Principles

* Separation of concerns
* Layered architecture
* Domain-driven structure (features)
* Containerized environment
* Scalable and maintainable

---

# 🚀 Summary

```id="summary"
apps/      → business logic
backend/   → API + DB
frontend/  → UI
infra/     → Docker + environment
```

---

# ⚙️ Requirements

* Docker
* Docker Compose

---

# 🚀 Getting Started

## 1. Clone repository

```
git clone <your-repo>
cd BFS_Life_OOA
```

---

## 2. Create `.env`

```
Read env.example
```

---

## 3. Run project

```
docker compose -f infra/docker/docker-compose.yml up --build
```

---

# 🌐 Services

| Service      | URL                        |
| ------------ | -------------------------- |
| Backend API  | http://localhost:8000      |
| Swagger Docs | http://localhost:8000/docs |
| Frontend     | http://localhost:3000      |

---

# 🗄 Database

PostgreSQL runs in Docker:

```
host: localhost
port: 5433
user: postgres
password: postgres
database: bfs
```

---

# 🔄 Migrations (Alembic)

## Create migration

```
docker exec -it bfs_backend alembic revision --autogenerate -m "message"
```

## Apply migrations

```
docker exec -it bfs_backend alembic upgrade head
```

---

# 🧹 Linting

З кореня репо (без локального Poetry / Node — усе в контейнерах):

```
make lint              # бек + фронт
make lint-backend      # Ruff (check + format --check)
make lint-frontend     # ESLint
```

Якщо вже піднятий `make run`, можна так:

## Backend (Ruff)

Run:

```
docker exec -it bfs_backend poetry run ruff check .
docker exec -it bfs_backend poetry run ruff format .
```

## Frontend (ESLint)

```
docker exec -it bfs_frontend npm run lint
```

---

# 🧪 Development Workflow

1. Start containers
2. Backend auto-reloads (uvicorn --reload)
3. Frontend auto-reloads (Vite)
4. Make changes → see instantly

---

# 🧠 Notes

* Backend uses async DB (asyncpg)
* Alembic uses sync DB (psycopg2)
* Migrations run automatically on startup
* Node version: 20+
* Python version: 3.11

---

# 🔥 Useful Commands

## Run project
```
make run
```


## Restart project

```
docker compose down
docker compose up --build
```

## Rebuild containers

```
docker compose build --no-cache
```

## Backend tests (pytest у Docker)

З кореня репо достатньо Docker. Команда сама підніме `db` (якщо не працює), дочекається Postgres, за потреби збере образ `backend` і запустить **одноразовий** контейнер з pytest (не треба окремо `make run`):

```
make test-backend
```

Використовується БД `bfs_test`; трафік на `db:5432` з asyncpg, як у проді.

## Enter backend container

```
docker exec -it bfs_backend bash
```

## Enter frontend container

```
docker exec -it bfs_frontend sh
```

---

# 🔁 CI Pipeline

Automated CI runs on every `push` and every `pull request` via GitHub Actions.

Pipeline includes:

* frontend build (`vite build`)
* frontend lint (`eslint`)
* frontend tests + coverage (`vitest`)
* backend lint (`ruff check` + `ruff format --check`)
* backend unit tests (`pytest tests/unit`)
* backend integration tests (`pytest tests/integration`)
* backend coverage reports (`coverage xml/html`)
* build/test/lint reports uploaded as workflow artifacts

Main workflow file:

```
.github/workflows/ci.yml
```

---

# 🏷 Versioning

Project uses **Semantic Versioning (SemVer)**:

```
MAJOR.MINOR.PATCH
```

Current version is stored in:

* root `VERSION`
* `apps/backend/pyproject.toml` (`tool.poetry.version`)
* `apps/frontend/package.json` (`version`)
* `apps/frontend/package-lock.json` (`version`)

Release rules:

* `PATCH` — bug fixes and non-breaking changes
* `MINOR` — new backward-compatible functionality
* `MAJOR` — breaking changes

Recommended release tag format:

```
vX.Y.Z
```

## Automated version bump

Use Make targets to bump version in all files automatically:

```
make version-patch   # X.Y.Z -> X.Y.(Z+1)
make version-minor   # X.Y.Z -> X.(Y+1).0
make version-major   # X.Y.Z -> (X+1).0.0
```

These commands sync:

* `VERSION`
* `apps/backend/pyproject.toml`
* `apps/frontend/package.json`
* `apps/frontend/package-lock.json`

## Automatic tag creation for release

If you want this to happen "automatically" as one command, use release targets:

```
make release-patch
make release-minor
make release-major
```

Each target:

* bumps version (SemVer)
* creates Git tag `vX.Y.Z`

Then push commits and tags:

```
git push
git push --tags
```

---

# 📌 Future Improvements

* User profiles
* Category management UI
* CI/CD pipeline

---

# 👨‍💻 Authors

Team BFS Life
