from abc import ABC, abstractmethod


class Queue(ABC):
    @property
    @abstractmethod
    def queue_name(self):
        pass

    @abstractmethod
    def on_message(self, _unused_channel, basic_deliver, properties, body):
        pass
