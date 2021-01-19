lint:
	poetry run flake8 differences_evaluator

install:
	python3 -m pip install --user dist/*.whl

test:
	poetry run pytest tests/

coverage:
	poetry run pytest --cov=differences_evaluator --cov-report xml tests/