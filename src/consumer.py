import time

import pika
from pika.adapters.asyncio_connection import AsyncioConnection

from dependencies.dependencies import save_email_use_case


class Consumer:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

        self.consuming = False
        self.was_consuming = False
        self.closing = False

        self.should_reconnect = False

    def connect(self) -> AsyncioConnection:
        return AsyncioConnection(
            parameters=pika.URLParameters(self.url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def close_connection(self):
        self.consuming = False
        if not self.connection.is_closing and not self.connection.is_closed:
            self.connection.close()

    def on_connection_open(self, _unused_connection):
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_open_error(self, _unused_connection, err):
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self.channel = None

        if self.closing:
            self.connection.ioloop.stop()
        else:
            self.reconnect()

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.queue_consume("reset_password")

    def on_channel_closed(self, channel, reason):
        self.close_connection()

    def queue_consume(self, queue_name):
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        print("in queue declare")
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.on_message, auto_ack=True
        )

        self.was_consuming = True
        self.consuming = True

    def on_consumer_cancelled(self, method_frame):
        if self.channel:
            self.channel.close()

    def stop_consuming(self):
        if self.channel:
            self.consuming = False
            self.channel.close()

    def on_message(channel, _unused_channel, basic_deliver, properties, body):
        save_email_use_case()(body)

    def run(self):
        self.connection = self.connect()
        self.connection.ioloop.run_forever()

    def stop(self):
        if not self.closing:
            self.closing = True
            if self.consuming:
                self.stop_consuming()
                self.connection.ioloop.run_forever()
            else:
                self.connection.ioloop.stop()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()


class ReconnectingConsumer:
    def __init__(self, amqp_url):
        self.reconnect_delay = 30
        self.amqp_url = amqp_url
        self.consumer = Consumer(self.amqp_url)

    def run(self):
        while True:
            try:
                self.consumer.run()
            except KeyboardInterrupt:
                self.consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self.consumer.should_reconnect:
            print("reconnection")
            self.consumer.stop()
            time.sleep(self.reconnect_delay)
            self.consumer = Consumer(self.amqp_url)
