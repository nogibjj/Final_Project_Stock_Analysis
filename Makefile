install:
	pip install --upgrade pip &&\
		pip install --prefer-binary -r requirements.txt

test:	
	python -m pytest -vv --cov=main *.py

format:
	black *.py
	
lint:
	ruff *.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

all: install test format lint
