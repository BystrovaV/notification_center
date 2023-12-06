from pymongo import MongoClient

from core.settings import Settings


class MongoDB:
    def __init__(self, client):
        self.client = client

    @classmethod
    def start(cls, settings: Settings):
        client = MongoClient(settings.get_mongodb_url())

        return cls(client)


class MongoDBRepository:
    def __init__(self, client: MongoClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def save_document(self, collection_name: str, body: dict):
        collection = self.db[collection_name]
        inserted_id = collection.insert_one(body).inserted_id
        return inserted_id
