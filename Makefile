lint:
	poetry run flake8 task_manager

test:
	poetry run pytest

test-local:
	poetry run python3 -m pytest

install:
	poetry install

dev:
	poetry run python manage.py runserver

check:
	make lint
	make test

test-coverage:
	poetry run python3 -m pytest --cov=task_manager --cov-report=xml

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-force-reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall