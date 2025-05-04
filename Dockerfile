# Stage 1: Base build stage
FROM python:3.13-slim

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Run using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "hotelhub.asgi:application"]
