run-tests:
	poetry run python -m pytest tests/ --color=yes -v

run-lint:
	poetry run flake8 --ignore E501 \
		--exclude .git,.venv,__pycache__,.pytest_cache,src/application/scraper \
		--max-complexity 12

run-formatter:
	poetry run black .