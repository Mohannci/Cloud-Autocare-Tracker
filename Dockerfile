# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY go_mechanic/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables from build arguments
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN
ARG AWS_REGION
ARG AWS_S3_BUCKET
ARG AWS_DYNAMODB_REGION
ARG AWS_SNS_TOPIC_ARN

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
ENV AWS_REGION=${AWS_REGION}
ENV AWS_S3_BUCKET=${AWS_S3_BUCKET}
ENV AWS_DYNAMODB_REGION=${AWS_DYNAMODB_REGION}
ENV AWS_SNS_TOPIC_ARN=${AWS_SNS_TOPIC_ARN}

# Collect static files and run migrations
RUN python go_mechanic/manage.py migrate --no-input
RUN python go_mechanic/manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "--workers=4", "--timeout=180", "--bind=0.0.0.0:8000", "backend.wsgi:application"]

