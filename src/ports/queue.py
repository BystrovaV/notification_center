from abc import ABC, abstractmethod


class Queue(ABC):
    @property
    @abstractmethod
    def queue_name(self) -> str:
        pass

    @abstractmethod
    def on_message(self, channel, basic_deliver, properties, body):
        pass
