```markdown
# Makefile Documentation

This project includes a `Makefile` to simplify the most common Django management commands.  
You can use these predefined commands by running `make` followed by the command name in your terminal.

## 📖 Usage

Open your terminal, navigate to the project directory where the `Makefile` is located, and run:

```bash
make <command>
```

Replace `<command>` with one of the available commands listed below.

## 📦 Available Commands

| Command          | Description                           |
|:----------------|:--------------------------------------|
| `runserver`      | Runs the Django development server.   |
| `makemigrations` | Creates new migration files.          |
| `migrate`        | Applies database migrations.          |
| `createsuperuser`| Creates a new Django superuser.       |
| `test`           | Runs the project’s unit tests.        |

## 📑 Example

To make migrations, apply them, and run the development server:

```bash
make makemigrations
make migrate
make runserver
```

To create a superuser:

```bash
make createsuperuser
```

To run tests:

```bash
make test
```

## 📁 Makefile Content

Below is the content of the `Makefile` used in this project:

```makefile
runserver:
	python manage.py runserver

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

test:
	python manage.py test
```

## ✅ Notes

- Make sure you have `make` installed on your system.
- Always run these commands from the directory where the `Makefile` and `manage.py` are located.
```