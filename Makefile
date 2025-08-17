.PHONY: build up down logs

build:
	docker-compose build

up: build
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f
.PHONY: up down build logs

build:
	docker-compose build

up: build
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f
