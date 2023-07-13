.PHONY: build

build: requirements

requirements:
	pip-compile requirements.in --no-header

clean:
	rm -rf venv

install:
	python -m venv venv
	( \
       . venv/bin/activate; \
       pip install -r requirements.txt; \
    )

docker-compose-up:
	echo "POSTGRES_HOST=localhost" > infra/.env
	echo "POSTGRES_PORT=5432" > .env
	echo "POSTGRES_USERNAME=postgres" >> .env
	echo "POSTGRES_PASSWORD=postgres" >> .env
	echo "POSTGRES_DB=postgres" >> .env
	docker-compose up -d