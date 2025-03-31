# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up the directory structure
WORKDIR /app

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r go_mechanic/requirements.txt
RUN pip install gunicorn

# Set environment variables
ENV PYTHONPATH=/app:/app/go_mechanic
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Run migrations
WORKDIR /app/go_mechanic
RUN python manage.py migrate --no-input

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port
EXPOSE 8000

# Entrypoint script
CMD ["gunicorn", "--workers=4", "--timeout=180", "--bind=0.0.0.0:8000", "backend.wsgi:application"]
