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
 
# Set environment variables before running collectstatic
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=go_mechanic.backend.settings
ENV PYTHONPATH=/app
ENV ROOT_URLCONF=go_mechanic.backend.urls
 
# Set AWS environment variables
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
ENV AWS_REGION=${AWS_REGION}
ENV AWS_S3_BUCKET=${AWS_S3_BUCKET}
ENV AWS_SNS_TOPIC_ARN=${AWS_SNS_TOPIC_ARN}
ENV AWS_DYNAMODB_REGION=${AWS_DYNAMODB_REGION}
 
# Collect static files (run from the go_mechanic directory with explicit path)
RUN python /app/go_mechanic/manage.py collectstatic --noinput
 
# Expose port
EXPOSE 8000
 
# Run migrations and start server
CMD ["sh", "-c", "cd /app/go_mechanic && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 go_mechanic.backend.wsgi:application"]
