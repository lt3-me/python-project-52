lint:
	poetry run flake8 task_manager

test:
	poetry run pytest

test-local:
	poetry run python3 -m pytest

install:
	poetry install

build:
	make install

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry run python manage.py migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

check:
	make lint
	make test

test-coverage:
	poetry run python3 -m pytest --cov=task_manager --cov-report=xml