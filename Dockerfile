# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 5050

# Set environment variables for production (override as needed)
ENV COOKIE_SECRET=your-secret-key-change-in-production

# Start the application
CMD ["python", "main.py"]
