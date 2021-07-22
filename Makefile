VENV := venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate

.PHONY: install
install: venv ## Make venv and install requirements
	$(BIN)/pip install --upgrade -r requirements.txt

freeze: ## Pin current dependencies
	$(BIN)/pip freeze > requirements.txt

migrate: ## Make and run migrations
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

del_migrations: ## delete all migration files
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "tripper/*/migrations/*.pyc"  -delete

erd: ## Make erd jpg in doc folder and dot file to edit in https://dreampuf.github.io/GraphvizOnline and 
	pip install django-extensions pygraphviz 
	python manage.py graph_models -a -g -o docs/ERD.png  
	python manage.py graph_models -a > docs/erd-dotfile.dot
	python manage.py show_urls > docs/urls.txt 
	pip uninstall django-extensions 
	pip uninstall pygraphviz 

db-up: ## Pull and start the Docker Postgres container in the background
	docker pull postgres
	docker-compose up -d

db-shell: ## Access the Postgres Docker database interactively with psql. Pass in DBNAME=<name>.
	docker exec -it container_name psql -d $(DBNAME)

.PHONY: test
test: ## Run tests
	$(PYTHON) manage.py test application --verbosity=0 --parallel --failfast

run-docker:
	docker-compose up

start-docker:
	cdocker-compose run web python manage.py makemigrations 
	docker-compose run web python manage.py migrate  
	docker-compose up --build

add-env:
	cat .env | export

.PHONY: run
run: ## Run the Django server
	$(PYTHON) manage.py runserver

start: install migrate run ## Install requirements, apply migrations, then start development server

make_locale_messages: 
	django-admin makemessages -l fa_IR  -i $(VENV) 