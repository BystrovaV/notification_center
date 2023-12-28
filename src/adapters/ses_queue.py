import json
import logging

import pika

from adapters.controller import EmailInput
from core.settings import Settings
from ports.queue import Queue
from use_case.email_use_case import SaveEmailUseCase


class SesQueue(Queue):
    def __init__(self, settings: Settings, use_case: SaveEmailUseCase):
        logging.info("init sesqueue")
        self.settings = settings
        self.use_case = use_case
        logging.info("after init")

    @property
    def queue_name(self) -> str:
        return self.settings.SES_QUEUE

    def on_message(self, channel, basic_deliver, properties, body):
        headers = properties.headers
        retry_count = headers.get("retry_count", 0) if headers else 0
        logging.info(retry_count)

        try:
            email = EmailInput(**json.loads(body.decode("utf-8")))

            self.use_case(email.to_entity())
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            logging.info("Successful delivery")
        except Exception as ex:
            logging.error(ex)
            logging.info("Delivery failed")

            if retry_count < self.settings.MAX_RETRY_COUNT:
                if headers:
                    headers["retry_count"] = retry_count + 1
                else:
                    headers = {"retry_count": 1}

                channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
                new_properties = pika.BasicProperties(headers=headers)
                channel.basic_publish(
                    exchange="",
                    routing_key=self.settings.SES_QUEUE,
                    body=body,
                    properties=new_properties,
                )
            else:
                channel.basic_reject(
                    delivery_tag=basic_deliver.delivery_tag, requeue=False
                )

    @property
    def exchange_name(self) -> str | None:
        return super().exchange_name

    @property
    def exchange_type(self) -> str:
        return super().exchange_type

    @property
    def exchange_routing_key(self) -> str:
        return super().exchange_routing_key

    @property
    def is_consume(self) -> bool:
        return True

    @property
    def is_durable(self) -> bool:
        return True

    @property
    def args(self) -> dict:
        return {
            "x-dead-letter-exchange": self.settings.DLQ_EXCHANGE,
            "x-dead-letter-routing-key": self.settings.DLQ_ROUTING_KEY,
        }
