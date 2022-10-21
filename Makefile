HOST := raspberrypi.local
SSH_USER := pi
SSH_KEY := ~/.ssh/id_rsa
CRON := */30 * * * *

.EXPORT_ALL_VARIABLES:

.PHONY: provision
provision : build
	docker compose run --rm ansible

.PHONY: shell
shell : build
	docker compose run --entrypoint '' --rm ansible bash

.PHONY: build
build :
	docker compose build --pull ansible
