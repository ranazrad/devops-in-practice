import os
import requests
import pandas as pd
import sqlalchemy
import pika
import json
import time
import logging
import pymysql  # MySQL Connector

# -----------------------
# Configuration and Setup
# -----------------------

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for database and message queue connections
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "mydb")
MQ_HOST = os.environ.get("MQ_HOST", "rabbitmq")
API_URL = "https://randomuser.me/api/?results=5"

# -----------------------
# ETL Process
# -----------------------

def wait_for_db():
    """
    Wait until the MySQL database is ready to accept connections.
    Retries the connection multiple times before raising an exception.
    """
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
            break
        except pymysql.err.OperationalError:
            logging.warning("Database not ready, waiting...")
            time.sleep(3)
    else:
        raise Exception("Database was not ready after multiple attempts.")

def extract_data(api_url):
    """
    Extract data from the randomuser.me API.

    Args:
        api_url (str): The API endpoint to fetch data from.

    Returns:
        list: A list of user data dictionaries.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()["results"]
        logging.info(f"Extracted {len(data)} records from API.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during data extraction: {e}")
        return []

def transform_data(data):
    """
    Transform the extracted data into a structured format suitable for loading into the database.

    Args:
        data (list): The raw user data extracted from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the transformed user data.
    """
    if not data:
        logging.warning("No data to transform.")
        return pd.DataFrame()

    records = []
    for user in data:
        record = {
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "email": user["email"],
            "country": user["location"]["country"],
            "username": user["login"]["username"]
        }
        records.append(record)
    df = pd.DataFrame(records)
    logging.info(f"Transformed data into DataFrame with {len(df)} records.")
    return df

def load_data(df):
    """
    Load the transformed data into the MySQL database.

    Args:
        df (pandas.DataFrame): The transformed user data.
    """
    if df.empty:
        logging.info("No data to load into the database.")
        return

    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
    )
    try:
        df.to_sql("users", engine, if_exists="replace", index=False)
        logging.info("Successfully loaded data into the 'users' table!")
    except Exception as e:
        logging.error(f"Error loading data into database: {e}")

def main():
    """
    Main function to orchestrate the ETL process.
    """
    # Wait for the database to be ready
    wait_for_db()

    # -----------------------
    # Extract
    # -----------------------
    # Extract data directly from the API
    raw_data = extract_data(API_URL)

    if not raw_data:
        logging.info("No data to process. Exiting ETL.")
        return

    # -----------------------
    # Transform
    # -----------------------
    transformed_data = transform_data(raw_data)

    # -----------------------
    # Load
    # -----------------------
    load_data(transformed_data)

if __name__ == "__main__":
    main()
