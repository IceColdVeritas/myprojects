# import pika
# import pandas as pd
# import csv
# import os
# import signal
# import time

# # Use the csv_file_path variable to read the CSV file in your code
# csv_file_path = os.environ['CSV_FILE_PATH']
# csv_file_name = os.path.basename(csv_file_path)
# output_file_name = "output.csv"

# # RabbitMQ connection parameters
# RABBITMQ_HOST = 'rabbitmq'
# RABBITMQ_PORT = 5672
# RABBITMQ_USERNAME = 'guest'
# RABBITMQ_PASSWORD = 'guest'
# RABBITMQ_QUEUE = 'csv_queue'

# def parse_csv_row(row):
#     parsed_row = []
#     is_within_quotes = False
#     current_field = ""

#     for data in row:
#         if is_within_quotes:
#             current_field += ',' + data
#             if current_field.endswith("'"):
#                 current_field = current_field[1:-1]  # Remove surrounding single quotes
#                 parsed_row.append(current_field)
#                 is_within_quotes = False
#                 current_field = ""
#         elif data.startswith("'") and not data.endswith("'"):
#             current_field += data
#             is_within_quotes = True
#         else:
#             parsed_row.append(data)

#     return parsed_row

# def callback(ch, method, properties, body):
#     message = body.decode('utf-8')
#     print(f"Received message: {message}")
#     parsed_row = parse_csv_row(message.split(','))
#     csv_data.append(parsed_row)

# def consume_csv_data():
#     time.sleep(7)  # Wait for 10 seconds before connecting to RabbitMQ
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(
#                 host=RABBITMQ_HOST,
#                 port=RABBITMQ_PORT,
#                 credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
#             )
#         )
#         channel = connection.channel()
#         channel.queue_declare(queue=RABBITMQ_QUEUE)
#         channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
#         channel.start_consuming()
#     except KeyboardInterrupt:
#         connection.close()
#         print("\nCSV consumption stopped by user.")

# if __name__ == '__main__':
#     csv_data = []
#     try:
#         consume_csv_data()
#     except KeyboardInterrupt:
#         print("\nCSV consumption stopped by user.")

#     # Create DataFrame from the received data
#     df = pd.DataFrame(csv_data)
#     print("\nDataFrame:")
#     print(df)

#     # Write CSV file
#     output_file = os.path.join(os.path.dirname(csv_file_path), output_file_name)
#     with open(output_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerows(csv_data)

#     print(f"\nCSV file '{output_file}' generated.")



# import pika
# import csv
# import pandas as pd
# import sys
# import signal
# import os

# output_filename = sys.argv[1]

# def handle_interrupt(signal, frame):
#     print('Stopping consumer...')
#     sys.exit(0)

# signal.signal(signal.SIGINT, handle_interrupt)

# def parse_message(message):
#     return message.decode().split(',')

# def create_dataframe(messages):
#     data = [parse_message(msg) for msg in messages]
#     return pd.DataFrame(data)

# def write_to_csv(df, output_file):
#     df.to_csv(output_file, index=False)

# def callback(ch, method, properties, body):
#     print(f'Received message: {body}')
#     with open(output_filename, 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([body.decode()])

# params = pika.ConnectionParameters('rabbitmq', 5672)
# connection = pika.BlockingConnection(params)
# channel = connection.channel()
# channel.queue_declare(queue='csv_queue')

# channel.basic_consume(queue='csv_queue', on_message_callback=callback, auto_ack=True)

# print('Starting consumer...')
# channel.start_consuming()

# print('Finished consuming messages')

# # generate signal to stop containers
# with open('/output_file_created', 'w') as signal_file:
#     signal_file.write('output file created')
#     signal_file.flush()
#     os.kill(os.getpid(), signal.SIGTERM)



import signal
import csv
import pandas as pd
import os
import sys
import pika

# RabbitMQ connection parameters
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_QUEUE = 'csv_queue'

# Use the output_file_path variable to set the path and filename for the output file
output_file_path = os.environ['OUTPUT_FILE_PATH']

# List to store the parsed CSV rows
csv_rows = []

def parse_csv_row(row):
    parsed_row = []
    for field in row:
        # Check if the field contains a comma
        if ',' in field:
            # Enclose the field in quotes to preserve commas
            parsed_row.append(f'"{field}"')
        else:
            parsed_row.append(field)
    return parsed_row

def callback(ch, method, properties, body):
    # Decode the message body and split into individual fields
    message = body.decode('utf-8')
    row = message.split(',')

    # Parse the row and append it to the csv_rows list
    parsed_row = parse_csv_row(row)
    csv_rows.append(parsed_row)

# Start consuming messages
def consume_csv_data():
    params = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    # Create a DataFrame from the csv_rows list
    df = pd.DataFrame(csv_rows)

    # Write the DataFrame to the output file
    df.to_csv(output_file_path, index=False)

    # Stop consuming messages and close the connection
    channel.stop_consuming()
    connection.close()

    # Stop the container
    sys.exit(0)

if __name__ == '__main__':
    csv_data = []
    try:
        consume_csv_data()
    except KeyboardInterrupt:
        print("\nCSV consumption stopped by user.")

    # Register the signal handlers for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, consume_csv_data)
    signal.signal(signal.SIGTERM, consume_csv_data)
