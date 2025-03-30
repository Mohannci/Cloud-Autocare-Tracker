# Use a minimal Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file from go_mechanic directory
COPY go_mechanic/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=go_mechanic.backend.settings
ENV PYTHONPATH=/app
ENV ROOT_URLCONF=go_mechanic.backend.urls

# Ensure static directory exists before collecting static files
RUN mkdir -p /app/go_mechanic/staticfiles && chmod -R 777 /app/go_mechanic/staticfiles

# Debug: Check installed packages
RUN pip list

# Collect static files
RUN python /app/go_mechanic/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "cd /app/go_mechanic && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 go_mechanic.backend.wsgi:application"]
