# Use an official Python runtime as the base image
FROM python:3.9-slim
 
# Set working directory to the project root
WORKDIR /app
 
# Copy requirements file from go_mechanic directory
COPY go_mechanic/requirements.txt .
 
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the entire project
COPY . /app
 
# Copy the .env file from the root directory to /app/go_mechanic
COPY .env /app/go_mechanic/.env
 
# Set environment variables before running collectstatic
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=go_mechanic.backend.settings
ENV PYTHONPATH=/app
ENV ROOT_URLCONF=go_mechanic.backend.urls
 
# Collect static files (run from the go_mechanic directory with explicit path)
RUN python /app/go_mechanic/manage.py collectstatic --noinput
 
# Expose port
EXPOSE 8000
 
# Run migrations and start server
CMD ["sh", "-c", "cd /app/go_mechanic && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 go_mechanic.backend.wsgi:application"]
 