# AWS App Runner optimized Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV AWS_DEFAULT_REGION=us-east-1

# Install system dependencies (removed curl since health check won't work in App Runner)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port (App Runner expects 8080 by default)
EXPOSE 8080

# Remove HEALTHCHECK - App Runner handles this differently
# App Runner will monitor your service through HTTP requests to your endpoints

# Run the application
CMD ["python", "llm_api.py"]