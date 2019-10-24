SHELL := /bin/bash

.PHONY: build
build:
	docker build \
		-t my-cool-timezone-app:local \
		-f ./Dockerfile .

.PHONY: test-integration
test-integration:
	docker-compose down
	docker-compose run timezone-app-behave /bin/bash -c '\
		set -e; \
		behave; \
	' || (docker-compose logs && exit 1)
