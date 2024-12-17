import os
import pandas as pd
import sqlalchemy
import pika
import json
import time
import logging
import pymysql

# ------------------------
# Configuration and Setup
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()
    ]
)

DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "mydb")
MQ_HOST = os.environ.get("MQ_HOST", "rabbitmq")

# ------------------------
# ETL Functions
# ------------------------
def wait_for_db():
    for attempt in range(10):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                port=3306
            )
            conn.close()
            logging.info("Database connection successful.")
            return
        except pymysql.err.OperationalError:
            logging.warning("Database not ready. Retrying...")
            time.sleep(5)
    raise Exception("Database not ready after multiple attempts.")

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue', durable=True)

    messages = []
    for method_frame, properties, body in channel.consume('users_queue', inactivity_timeout=5):
        if body is None:
            break
        messages.append(json.loads(body))
        channel.basic_ack(method_frame.delivery_tag)

    connection.close()
    logging.info(f"Consumed {len(messages)} messages from RabbitMQ.")
    return messages

def transform_data(data):
    if not data:
        return pd.DataFrame()
    return pd.DataFrame([
        {
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "email": user["email"],
            "country": user["location"]["country"],
            "username": user["login"]["username"]
        }
        for user in data
    ])

def load_data(df):
    if df.empty:
        logging.info("No data to load.")
        return
    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )

    with engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                country VARCHAR(50),
                username VARCHAR(50)
            )
        """))

    # Append data to the table without deduplication
    df.to_sql("users", engine, if_exists="append", index=False)
    logging.info("Data appended successfully into MySQL.")


def main():
    wait_for_db()
    raw_data = consume_messages()
    if not raw_data:
        logging.info("No data to process. Exiting.")
        return
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)

if __name__ == "__main__":
    main()
