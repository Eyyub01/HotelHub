runserver:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput

test:
	python manage.py test

shell:
	python manage.py shell

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

help:
	@echo "Available commands:"
	@echo "  runserver         - Start the Django development server"
	@echo "  migrate           - Apply database migrations"
	@echo "  makemigrations    - Create new database migrations"
	@echo "  createsuperuser   - Create a new superuser"
	@echo "  collectstatic     - Collect static files"
	@echo "  test              - Run tests"
	@echo "  shell             - Open the Django shell"
	@echo "  clean             - Remove .pyc files and __pycache__ directories"
	@echo "  manage cmd=<cmd>  - Run any manage.py command (e.g., make manage cmd=showmigrations)"