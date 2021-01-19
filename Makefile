lint:
	poetry run flake8 differences_evaluator

package-install:
	python3 -m pip install --user dist/*.whl

install:
	poetry install

test:
	poetry run pytest tests/

coverage:
	poetry run pytest --cov=differences_evaluator --cov-report xml tests/