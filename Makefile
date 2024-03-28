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

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

dev:
	make migrations
	make migrate
	poetry run python manage.py runserver

PORT ?= 8000
start:
	make migrations
	make migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

check:
	make lint
	make test

test-coverage:
	poetry run python3 -m pytest --cov=task_manager --cov-report=xml