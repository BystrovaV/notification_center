import logging
import time

import pika
from pika.adapters.asyncio_connection import AsyncioConnection

from ports.queue import Queue

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, url: str, queues: list[Queue]):
        self.url = url
        self.connection = None
        self.channel = None

        self.consuming = False
        self.closing = False

        self.should_reconnect = False

        self.queues = queues

    def connect(self) -> AsyncioConnection:
        logger.info("Create connection")

        return AsyncioConnection(
            parameters=pika.URLParameters(self.url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def close_connection(self):
        self.consuming = False
        if not self.connection.is_closing and not self.connection.is_closed:
            logger.info("Close connection")
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
        self.queue_consume()

    def on_channel_closed(self, channel, reason):
        self.close_connection()

    def queue_consume(self):
        self.channel.basic_qos(prefetch_count=1)

        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)

        # --------------------
        logger.info("Declare queue")
        for queue in self.queues:
            self.channel.queue_declare(queue=queue.queue_name)
            self.channel.basic_consume(
                queue=queue.queue_name,
                on_message_callback=queue.on_message,
                # auto_ack=True,
            )
        # --------------------

        self.consuming = True

    def on_consumer_cancelled(self, method_frame):
        if self.channel:
            logger.info("Close channel")
            self.channel.close()

    def stop_consuming(self):
        if self.channel:
            self.consuming = False
            self.channel.close()

    # def on_message(self, channel, _unused_channel, basic_deliver, properties, body):
    # save_email_use_case()(body)

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
    def __init__(self, amqp_url, queues: list[Queue]):
        self.reconnect_delay = 30
        self.amqp_url = amqp_url
        self.consumer = Consumer(self.amqp_url, queues)

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
            logger.info("Reconnect to rabbitmq")
            self.consumer.stop()
            time.sleep(self.reconnect_delay)
            self.consumer = Consumer(self.amqp_url, self.consumer.queues)
