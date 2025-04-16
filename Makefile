runserver:
	python manage.py runserver

make:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

test:
	python manage.py test