from __future__ import (
    absolute_import,
    division,
    print_function,
)

from functools import partial
# Unix env library
import os
# AMQP client library
import pika

import random
import time

# Name of the RABBITMQ exchange
EXCHANGE = "exchange"

# AMQP routing key when we send the message
ROUTING_KEY = "wiki_updates"

# Delay between sending messages
sleep_time = random.uniform(0, 1)
DELAY = time.sleep(sleep_time)

file = "/Users/fideltewolde/training/myprojects/storage/de_challenge_sample_data.csv"
with open(file, "rb") as csv_file:
    wiki_updates = csv_file.read()


def main():

    # get location of AMQP broker
    amqp_url = os.environ["AMQP_URL"]
    print("URL: %s" % (amqp_url))

    # Connect to AMQP broker
    params = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(params, on_open_callback=on_open)

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


def on_open(connection):
    print("Connected")
    connection.channel(on_channel_open)


def on_channel_open(channel):
    # Callback for open channel on connection
    print("have channel")
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="fanout",
                             durable=True,
                             callback=partial(on_exchange, channel))


def on_exchange(channel, frame):
    # Callback for successfully declaring exchange
    print("Have exchange")
    send_message(channel, wiki_updates)


def send_message(channel, msg):
    # Send message to queue plus timeout

    print(msg)
    channel.basic_publish(EXCHANGE, ROUTING_KEY, msg,
                          pika.BasicProperties(content_type="text/plain",
                                               delivery_mode=2))
    channel.connection.add_timeout(DELAY, partial(send_message, channel))


if __name__=="__main__":
    main()