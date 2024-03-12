build-ci:
	python -m pip install --upgrade pip \
	pip install poetry \
	poetry install --with dev \

run-tests:
	poetry run python -m pytest tests/

run-lint:
	poetry run flake8 --ignore E501 \
		--exclude .git,__pycache__,.pytest_cache,src/application/scraper \
		--max-complexity 10
