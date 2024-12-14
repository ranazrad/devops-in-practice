import os
import requests
import pandas as pd

# -----------------------
# Configuration and Setup
# -----------------------

# API URL
API_URL = "https://randomuser.me/api/?results=5"

# -----------------------
# ETL Process
# -----------------------

def extract_data():
    """
    Extract data from the randomuser.me API.

    Returns:
        list: A list of user data dictionaries.
    """
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()["results"]
    print(f"Extracted {len(data)} records from API.")
    return data

def transform_data(data):
    """
    Transform the extracted data into a structured format suitable for analysis.

    Args:
        data (list): The raw user data extracted from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the transformed user data.
    """
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
    print(f"Transformed data into DataFrame with {len(df)} records.")
    return df

def main():
    """
    Main function to orchestrate the ETL process.
    """
    # -----------------------
    # Extract
    # -----------------------
    raw_data = extract_data()

    # -----------------------
    # Transform
    # -----------------------
    transformed_data = transform_data(raw_data)

    # -----------------------
    # Output Results
    # -----------------------
    print("\nTransformed Data:")
    print(transformed_data)

if __name__ == "__main__":
    main()
