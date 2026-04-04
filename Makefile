COMPOSE := infra/docker/docker-compose.yml

.PHONY: run down build-nocache lint lint-backend lint-frontend test-backend

down:
	docker compose -f $(COMPOSE) down

run:
	docker compose -f $(COMPOSE) up --build --force-recreate backend frontend

build-nocache:
	docker compose -f $(COMPOSE) build --no-cache backend

# Піднімає лише Postgres (якщо ще не працює), чекає готовності, створює bfs_test,
# збирає образ backend за потреби й одноразово запускає pytest (не потрібен запущений uvicorn).
test-backend:
	docker compose -f $(COMPOSE) up -d db
	@until docker compose -f $(COMPOSE) exec -T db pg_isready -U postgres -d bfs >/dev/null 2>&1; do sleep 1; done
	docker compose -f $(COMPOSE) exec -T db psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'bfs_test'" | grep -q 1 || docker compose -f $(COMPOSE) exec -T db psql -U postgres -c "CREATE DATABASE bfs_test;"
	docker compose -f $(COMPOSE) run --rm --build --no-deps backend sh -lc "cd /app && poetry run pytest tests/ -q"

# Ruff / ESLint у Docker — локальний Poetry / Node не потрібні.
lint-backend:
	docker compose -f $(COMPOSE) run --rm --build --no-deps backend sh -lc "cd /app && poetry run ruff check . && poetry run ruff format --check ."

lint-frontend:
	docker compose -f $(COMPOSE) run --rm --build --no-deps frontend sh -lc "npm run lint"

lint: lint-backend lint-frontend
