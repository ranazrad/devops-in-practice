import pika
import json
import time
import os

MQ_HOST = os.environ.get("MQ_HOST", "rabbitmq")

def publish_message(user):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='users_queue',
        body=json.dumps(user),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

if __name__ == "__main__":
    users = [
        {"name": {"first": "Alice", "last": "Smith"}, "email": "alice@example.com", "location": {"country": "USA"}, "login": {"username": "alice1"}},
        {"name": {"first": "Bob", "last": "Brown"}, "email": "bob@example.com", "location": {"country": "Canada"}, "login": {"username": "bob2"}}
    ]
    for user in users:
        publish_message(user)
        time.sleep(1)
