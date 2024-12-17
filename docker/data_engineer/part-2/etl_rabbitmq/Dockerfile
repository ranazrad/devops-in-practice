FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY etl.py .
COPY producer.py .

ENV DB_USER=user
ENV DB_PASS=password
ENV DB_HOST=db
ENV DB_NAME=mydb
ENV MQ_HOST=rabbitmq

CMD ["python", "etl.py"]
