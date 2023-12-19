import logging

from adapters.mongodb import MongoDB, MongoDBRepository
from core.settings import get_settings


class MongoDBDependency:
    def __init__(self):
        self.mongodb = None

    def __call__(self) -> MongoDB:
        settings = get_settings()
        self.mongodb = MongoDB.start(settings) if not self.mongodb else self.mongodb
        return self.mongodb


def get_mongodb_client():
    mongodb = MongoDBDependency()()
    # with mongodb.client.start_session() as session:
    # with session.start_transaction():
    # yield mongodb.client
    return mongodb.client


def get_mongodb_repository() -> MongoDBRepository:
    logging.info("create mongobd repository")
    client = get_mongodb_client()
    settings = get_settings()
    logging.info("create mongobd repository")
    return MongoDBRepository(client, settings.DB_NAME)
