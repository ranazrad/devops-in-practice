import pika
import json
import time
import os
import requests
import sys

MQ_HOST = os.environ.get("MQ_HOST", "rabbitmq")
USER_COUNT = int(os.environ.get("USER_COUNT", 1))  # Default to 1 user

def fetch_users(count=1):
    """Fetch user data from randomuser.me API."""
    url = f"https://randomuser.me/api/?results={count}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching user data: {e}")
        return []

def publish_message(user):
    """Publish a single user message to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='users_queue',
        body=json.dumps(user),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[x] Sent user: {user['login']['username']}")
    connection.close()

if __name__ == "__main__":
    # Allow dynamic user count from the command line
    if len(sys.argv) > 1:
        try:
            USER_COUNT = int(sys.argv[1])
        except ValueError:
            print("Invalid number of users provided. Using default USER_COUNT.")
    
    print(f"Fetching {USER_COUNT} users...")
    users = fetch_users(USER_COUNT)

    for user in users:
        publish_message(user)
        time.sleep(1)

    print("[x] All messages sent!")
