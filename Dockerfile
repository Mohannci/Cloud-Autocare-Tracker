# Use a minimal Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY go_mechanic/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=go_mechanic.backend.settings \
    PYTHONPATH=/app \
    ROOT_URLCONF=go_mechanic.backend.urls \
    AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

# Ensure static directory exists before collecting static files
RUN mkdir -p /app/go_mechanic/staticfiles && chmod -R 777 /app/go_mechanic/staticfiles

# Collect static files
RUN python /app/go_mechanic/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start the application
CMD ["sh", "-c", "cd /app/go_mechanic && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 go_mechanic.backend.wsgi:application"]
