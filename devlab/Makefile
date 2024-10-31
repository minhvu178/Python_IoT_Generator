
.DEFAULT_GOAL := help
include .env

define HELP

Available commands:

- run: This will call core.

- down: Tear down the project, clean directories.

- ps: Show all running containers.

- logs: Show logs.
- logsf: Show logs with -f

- watch: Watch logs.


endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help

run:
	docker compose -p timeseries up -d mongodb 

down:	
	docker compose down
	cd data; rm -rf mongodb 

ps:
	docker compose ps

logs:
	docker compose logs

logsf:
	docker compose logs -f

watch:
	watch docker compose ps

