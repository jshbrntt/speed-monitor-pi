RPI_ADDR := 192.168.1.16

.EXPORT_ALL_VARIABLES:

.PHONY: provision
provision : build
	docker compose run --rm ansible

.PHONY: build
build :
	docker compose build ansible
