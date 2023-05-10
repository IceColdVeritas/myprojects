# import signal
# import csv
# import pandas as pd
# import os
# import sys
# import pika

# # RabbitMQ connection parameters
# RABBITMQ_HOST = 'rabbitmq'
# RABBITMQ_PORT = 5672
# RABBITMQ_USERNAME = 'guest'
# RABBITMQ_PASSWORD = 'guest'
# RABBITMQ_QUEUE = 'csv_queue'

# # Use the output_file_path variable to set the path and filename for the output file
# output_file_path = os.environ['OUTPUT_FILE_PATH']

# # List to store the parsed CSV rows
# csv_rows = []

# def parse_csv_row(row):
#     parsed_row = []
#     for field in row:
#         # Check if the field contains a comma
#         if ',' in field:
#             # Enclose the field in quotes to preserve commas
#             parsed_row.append(f'"{field}"')
#         else:
#             parsed_row.append(field)
#     return parsed_row

# def callback(ch, method, properties, body):
#     # Decode the message body and split into individual fields
#     message = body.decode('utf-8')
#     row = message.split(',')

#     # Parse the row and append it to the csv_rows list
#     parsed_row = parse_csv_row(row)
#     csv_rows.append(parsed_row)

# # Start consuming messages
# def consume_csv_data():
#     params = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT)
#     connection = pika.BlockingConnection(params)
#     channel = connection.channel()
#     channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
#     channel.start_consuming()

#     # Create a DataFrame from the csv_rows list
#     df = pd.DataFrame(csv_rows)

#     # Write the DataFrame to the output file
#     df.to_csv(output_file_path, index=False)

#     # Stop consuming messages and close the connection
#     channel.stop_consuming()
#     connection.close()

#     # Stop the container
#     sys.exit(0)

# if __name__ == '__main__':
#     csv_data = []
#     try:
#         consume_csv_data()
#     except KeyboardInterrupt:
#         print("\nCSV consumption stopped by user.")

#     # Register the signal handlers for SIGINT and SIGTERM
#     signal.signal(signal.SIGINT, consume_csv_data)
#     signal.signal(signal.SIGTERM, consume_csv_data)


import csv
import pandas as pd
import os
import signal
import pika
import atexit

# RabbitMQ connection parameters
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_QUEUE = 'csv_queue'

class CsvConsumer:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path
        self.csv_rows = []
        self.connection = None
        self.channel = None

    def parse_csv_row(self, row):
        parsed_row = []
        for field in row:
            # Check if the field contains a comma
            if ',' in field:
                # Enclose the field in quotes to preserve commas
                parsed_row.append(f'"{field}"')
            else:
                parsed_row.append(field)
        return parsed_row

    def callback(self, ch, method, properties, body):
        # Decode the message body and split into individual fields
        message = body.decode('utf-8')
        row = message.split(',')

        # Parse the row and append it to the csv_rows list
        parsed_row = self.parse_csv_row(row)
        self.csv_rows.append(parsed_row)

    def consume_csv_data(self):
        params = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, credentials=pika.credentials.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD))
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def create_output_file(self):
        # Create a DataFrame from the csv_rows list
        df = pd.DataFrame(self.csv_rows)

        # Write the DataFrame to the output file
        df.to_csv(self.output_file_path, index=False)

    def stop_consuming(self):
        if self.channel:
            self.create_output_file()
            self.channel.stop_consuming()
        if self.connection:
            self.create_output_file()
            self.connection.close()

def handle_termination(consumer):
    consumer.stop_consuming()

if __name__ == '__main__':
    output_file_path = os.environ['OUTPUT_FILE_PATH']
    consumer = CsvConsumer(output_file_path)
    atexit.register(handle_termination, consumer)

    try:
        consumer.consume_csv_data()
    except pika.exceptions.AMQPConnectionError:
        print("Failed to establish connection to RabbitMQ server.")
