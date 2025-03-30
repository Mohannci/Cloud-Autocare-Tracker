# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up the directory structure
WORKDIR /app

# Copy the entire project
COPY . .

# Create necessary __init__.py files to make directories proper Python packages
RUN find . -type d -not -path "*/\.*" -exec touch {}/__init__.py \;

# Install dependencies
RUN pip install --no-cache-dir -r go_mechanic/requirements.txt

# Install additional dependencies that might be needed
RUN pip install gunicorn

# Set PYTHONPATH to include both the root directory and the go_mechanic directory
ENV PYTHONPATH=/app:/app/go_mechanic

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Run migrations from the go_mechanic directory
WORKDIR /app/go_mechanic
RUN python manage.py migrate --no-input

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Create a simple entrypoint script
RUN echo '#!/bin/bash\n\
cd /app/go_mechanic\n\
exec gunicorn --workers=4 --timeout=180 --bind=0.0.0.0:8000 backend.wsgi:application\n\
' > /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
