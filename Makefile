install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:	
	find . -type f -name "*.py" -exec black {} \;
	find . -type f -name "*.ipynb" -exec nbqa black {} \;
		 
lint:
	find . -type f -name "*.py" -exec ruff check {} \;
	find . -type f -name "*.ipynb" -exec nbqa ruff {} \;

test:
	python -m pytest -vv  test_*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

all: install test format lint
