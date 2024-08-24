# Dockerfile for processor service
FROM python:3.9-slim

WORKDIR /app

# Install dependencies for psycopg2, pg_isready, and curl
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    postgresql-client \
    curl  # Install curl

# Copy application code and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY processor.py /app/processor.py

# Run the processor
CMD ["python", "processor.py"]
