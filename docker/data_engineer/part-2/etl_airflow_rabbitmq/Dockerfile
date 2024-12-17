# Stage 1: Build Stage
FROM python:3.9-slim AS builder
WORKDIR /app

# Install build dependencies for cryptography and others
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        gcc \
        musl-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime Stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY etl.py .
COPY producer.py .
ENV DB_USER=user
ENV DB_PASS=password
ENV DB_HOST=db
ENV DB_NAME=mydb
ENV MQ_HOST=rabbitmq
CMD ["python", "etl.py"]
