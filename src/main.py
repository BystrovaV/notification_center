from consumer import ReconnectingConsumer
from core.settings import get_settings

settings = get_settings()
consumer = ReconnectingConsumer(settings.get_rabbitmq_url())
consumer.run()
