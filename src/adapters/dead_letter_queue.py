from core.settings import Settings
from ports.queue import Queue


class DeadLetterQueue(Queue):
    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def queue_name(self) -> str:
        return self.settings.DLQ_QUEUE

    def on_message(self, channel, basic_deliver, properties, body):
        pass

    @property
    def exchange_name(self) -> str | None:
        return self.settings.DLQ_EXCHANGE

    @property
    def exchange_type(self) -> str:
        return "direct"

    @property
    def exchange_routing_key(self) -> str:
        return self.settings.DLQ_ROUTING_KEY

    @property
    def is_consume(self) -> bool:
        return False

    @property
    def is_durable(self) -> bool:
        return True

    @property
    def args(self) -> dict:
        return {}
