COMPOSE := infra/docker/docker-compose.yml
VERSION := $(shell cat VERSION)

.PHONY: run down build-nocache lint lint-backend lint-frontend test-backend \
	version-patch version-minor version-major tag-version \
	release-patch release-minor release-major \
	ci-prepare-reports ci-frontend-lint ci-frontend-test ci-frontend-build \
	ci-backend-lint ci-backend-test db-test-prepare

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

ci-prepare-reports:
	mkdir -p apps/frontend/reports apps/backend/reports

ci-frontend-lint: ci-prepare-reports
	docker compose -f $(COMPOSE) run --rm --build --no-deps frontend sh -lc 'cd /app && npx eslint . -f stylish > reports/eslint.log 2>&1; code=$$?; cat reports/eslint.log; npx eslint . -f json -o reports/eslint-report.json || true; exit $$code'

ci-frontend-test:
	docker compose -f $(COMPOSE) run --rm --build --no-deps frontend sh -lc "cd /app && npm run test:coverage -- --coverage.reporter=text --coverage.reporter=lcov --coverage.reporter=json-summary"

ci-frontend-build: ci-prepare-reports
	docker compose -f $(COMPOSE) run --rm --build --no-deps frontend sh -lc "cd /app && npm run build && du -sh dist > reports/build-size.txt && ls -la dist > reports/build-files.txt"

db-test-prepare:
	docker compose -f $(COMPOSE) up -d db
	@until docker compose -f $(COMPOSE) exec -T db pg_isready -U postgres -d bfs >/dev/null 2>&1; do sleep 1; done
	docker compose -f $(COMPOSE) exec -T db psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'bfs_test'" | rg -q 1 || docker compose -f $(COMPOSE) exec -T db psql -U postgres -c "CREATE DATABASE bfs_test;"

ci-backend-lint: ci-prepare-reports
	docker compose -f $(COMPOSE) run --rm --build --no-deps backend sh -lc 'cd /app && poetry run ruff check . > reports/ruff.log 2>&1; code=$$?; cat reports/ruff.log; poetry run ruff check . --output-format=json > reports/ruff-report.json || true; poetry run ruff format --check . | tee reports/ruff-format.log; exit $$code'

ci-backend-test: db-test-prepare ci-prepare-reports
	docker compose -f $(COMPOSE) run --rm --build --no-deps backend sh -lc "cd /app && poetry run python -m pip install coverage >/dev/null && poetry run coverage run -m pytest tests/unit -q --junitxml=reports/junit-unit.xml && poetry run coverage run -a -m pytest tests/integration -q --junitxml=reports/junit-integration.xml && poetry run coverage report -m > reports/coverage-summary.txt && poetry run coverage xml -o reports/coverage.xml && poetry run coverage html -d reports/coverage-html"

version-patch:
	python3 scripts/bump_version.py patch

version-minor:
	python3 scripts/bump_version.py minor

version-major:
	python3 scripts/bump_version.py major

tag-version:
	git tag "v$(VERSION)"
	@echo "Created tag v$(VERSION)"

release-patch: version-patch tag-version

release-minor: version-minor tag-version

release-major: version-major tag-version
