# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY go_mechanic/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the entire project
COPY . .

# Set the PYTHONPATH
ENV PYTHONPATH="/app:/app/go_mechanic"

# Run Django migrations
RUN python go_mechanic/manage.py migrate --no-input

# Collect static files
RUN python go_mechanic/manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Define the entrypoint
CMD ["gunicorn", "--workers=4", "--timeout=180", "--bind=0.0.0.0:8000", "backend.wsgi:application"]
