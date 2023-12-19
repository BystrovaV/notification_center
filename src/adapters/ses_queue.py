import logging

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
    def queue_name(self):
        return self.settings.SES_QUEUE

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        print(body)
        # return self.use_case(body)
