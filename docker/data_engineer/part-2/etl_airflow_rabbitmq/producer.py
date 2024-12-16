import pika
import json
import os
import time

MQ_HOST = os.environ.get("MQ_HOST", "rabbitmq")

def publish_message(user):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='users_queue',
        body=json.dumps(user),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print("Sent user data to users_queue")
    connection.close()

if __name__ == "__main__":
    sample_users = [
        {
            "name": {"first": "Alice", "last": "Johnson"},
            "email": "alice.johnson@example.com",
            "location": {"country": "UK"},
            "login": {"username": "alicej"}
        },
        {
            "name": {"first": "Bob", "last": "Williams"},
            "email": "bob.williams@example.com",
            "location": {"country": "Australia"},
            "login": {"username": "bobw"}
        }
    ]

    for user in sample_users:
        publish_message(user)
        time.sleep(1)
