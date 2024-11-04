.PHONY: migrate
migrate:
	docker exec -it salesrevv-fitness-agent-api-1 /bin/bash -c "alembic upgrade head"
