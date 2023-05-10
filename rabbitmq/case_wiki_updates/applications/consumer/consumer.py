from functools import partial
import os
import pika


EXCHANGE = "exchange"

QUEUE = "wiki_updates"


def main():

    # Get location of AMQP broker (RABBITMQ server).
    amqp_url = os.environ["AMQP_URL"]
    print("URL: %s" % (amqp_url))

    # Connect to AMQP broker.
    params = pika.URLParameters(amqp_url)
    connection  =pika.SelectConnection(params, on_open_callback=on_open)

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


def on_open(connection):
    # Callback for successfully connecting to the AMQP broker.
    print("Connected")
    connection.channel(on_channel_open)


def on_channel_open(channel):
    # Callback for successfully opening a channel to the connection.
    print("Have channel")

    # An exchange must be declared before binding it.
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="fanout",
                             durable=True,
                             callback=partial(on_exchange, channel))


def on_exchange(channel, frame):
    # Callback for successfully declaring the exchange.
    print("Have exchange")
    channel.queue_declare(queue=QUEUE, durable=True,
                          callback=partial(on_queue, channel))


def on_queue(channel, frame):
    # Callback for successfully declaring the queue.
    print("Have queue")

    # This call tells the server to send us 1 message in advance.
    channel.basic_qos(prefetch_count=1, callback=partial(on_qos, channel))


def on_qos(channel, frame):
    # Callback for the channel prefetch limit.
    print("Set QoS")
    channel.queue_bind(queue=QUEUE, exchange=EXCHANGE,
                       callback=partial(on_bind, channel))


def on_bind(channel, frame):
    # Callback for successfully binding the queue to the exchange.
    print("Bound")
    channel.basic_consume(queue=QUEUE, consumer_callback=on_message)


def on_message(channel, delivery, properties, body):
    # Callback when a message arrives.
    print("Exchange: %s" % (delivery.exchange))
    print("Routing key: %s" % (delivery.routing_key))
    print("Content type: %s" % (properties.content_type))
    
    channel.basic_ack(delivery.delivery_tag)


if __name__=="__main__":
    main()