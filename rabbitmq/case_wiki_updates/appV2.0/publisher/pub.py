import pika
import csv
import time
from random import random

import os

# Use the csv_file_path variable to read the CSV file in your code
csv_file_path = os.environ['CSV_FILE_PATH']
csv_file_name = os.path.basename(csv_file_path)

# RabbitMQ connection parameters
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_QUEUE = 'csv_queue'

def publish_csv_data():
    # time.sleep(7)
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)

        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                message = ','.join(row)
                channel.basic_publish(
                    exchange='',
                    routing_key=RABBITMQ_QUEUE,
                    body=message.encode('utf-8')
                )
                print(f"Sent message: {message}")

                time.sleep(random())  # Introduce a random time delay between 0 and 1 second

        connection.close()
    except pika.exceptions.AMQPConnectionError:
        print("Error: Failed to establish connection to RabbitMQ server.")

if __name__ == '__main__':
    publish_csv_data()
