# Makefile for project
.PHONY: clean-pyc clean-build docs

APP = ops
STATIC_DIR = static/

env:
	@bash entry.sh

migrate:
	@python manage.py makemigrations
	@python manage.py migrate 

createuser:
	@echo "Login Username: " admin
	@python manage.py createsuperuser --username admin --email admin@51reboot.com

run:
	@python manage.py runserver 0.0.0.0:9000
