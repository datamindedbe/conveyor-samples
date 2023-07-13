.PHONY: build

build: requirements

requirements:
	pip-compile requirements.in --no-header
	pip-compile dev-requirements.in --no-header

clean:
	rm -rf venv


test:
	( \
       . venv/bin/activate; \
       python -m pytest --cov=src tests; \
    )

install:
	python -m venv venv
	( \
       . venv/bin/activate; \
       pip install -r requirements.txt; \
       pip install -r dev-requirements.txt; \
       pip install -e .; \
    )