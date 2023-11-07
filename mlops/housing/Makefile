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
       pip install -e .; \
    )