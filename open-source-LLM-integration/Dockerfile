FROM python:3.11-slim

WORKDIR /app

# Update system packages and install ca-certificates
RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update pip and setuptools first
RUN pip install --upgrade pip setuptools

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages with trusted hosts (fallback for SSL issues)
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Copy application code
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Run the application
CMD ["python3", "llm_api.py"]