lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/*
	poetry run coverage xml --include=task_manager/*

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
