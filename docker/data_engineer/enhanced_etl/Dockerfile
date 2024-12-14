# Stage 1: Build Stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        gcc \
        musl-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime Stage
FROM python:3.9-slim

WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the ETL script
COPY etl.py .

# Set environment variables (optional: can be overridden by docker-compose)
ENV DB_USER=user
ENV DB_PASS=password
ENV DB_HOST=db
ENV DB_NAME=mydb

# Execute the ETL script
CMD ["python", "etl.py"]
