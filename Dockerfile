# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up the directory structure
WORKDIR /app

# Install dependencies first (improves caching)
COPY go_mechanic/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install gunicorn

# Copy the entire project
COPY . /app

# Set environment variables for Django
ENV PYTHONPATH="/app:/app/go_mechanic"
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Run migrations and collect static files
WORKDIR /app/go_mechanic
RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Entrypoint script
CMD ["gunicorn", "--workers=4", "--timeout=180", "--bind=0.0.0.0:8000", "backend.wsgi:application"]
