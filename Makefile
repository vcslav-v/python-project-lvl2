lint:
	poetry run flake8 gendiff

package-install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ vaclav_gendiff_training_project

install:
	poetry install

test:
	poetry run pytest tests/

coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests/