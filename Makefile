lint:
	poetry run flake8 gendiff

package-install:
	python3 -m pip install --user dist/*.whl

install:
	poetry install

test:
	poetry run pytest tests/

coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests/