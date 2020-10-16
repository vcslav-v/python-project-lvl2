lint:
	poetry run flake8 differences_evaluator

install:
	poetry install

test:
	poetry run pytest tests/differences_evaluator.py

coverage:
	poetry run coverage run -m pytest tests/differences_evaluator.py