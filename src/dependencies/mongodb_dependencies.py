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
    return mongodb.client()


def get_mongodb_repository() -> MongoDBRepository:
    client = get_mongodb_client()
    return MongoDBRepository(client)
