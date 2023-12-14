import logging.config

from consumer import ReconnectingConsumer
from core.settings import get_settings
from dependencies.dependencies import list_queue

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

settings = get_settings()
list_q = list_queue()
logging.info("Create list_q")
consumer = ReconnectingConsumer(settings.get_rabbitmq_url(), list_q)
consumer.run()
