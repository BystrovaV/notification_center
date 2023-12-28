from abc import ABC, abstractmethod


class Queue(ABC):
    @property
    @abstractmethod
    def queue_name(self) -> str:
        pass

    @property
    @abstractmethod
    def exchange_name(self) -> str | None:
        return None

    @property
    @abstractmethod
    def exchange_type(self) -> str:
        return "direct"

    @property
    @abstractmethod
    def exchange_routing_key(self) -> str:
        return ""

    @property
    @abstractmethod
    def is_consume(self) -> bool:
        return False

    @property
    @abstractmethod
    def is_durable(self) -> bool:
        return True

    @abstractmethod
    def on_message(self, channel, basic_deliver, properties, body):
        pass

    @property
    @abstractmethod
    def args(self) -> dict:
        return {}
