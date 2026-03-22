run:
	docker compose -f infra/docker/docker-compose.yml up --build

lint:
	cd apps/backend && ruff check .
	cd apps/frontend && npm run lint