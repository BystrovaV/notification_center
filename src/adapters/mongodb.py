import logging

from bson import ObjectId
from pymongo import MongoClient
from pymongo.cursor import Cursor

from core.exceptions import MongoDBConnectionException
from core.settings import Settings
from ports.repository import DocumentRepository

logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self, client: MongoClient):
        self.client = client

    @classmethod
    def start(cls, settings: Settings):
        logger.info("Create mongo client")
        client = MongoClient(settings.get_mongodb_url())

        return cls(client)


class MongoDBRepository(DocumentRepository):
    def __init__(self, client: MongoClient, db_name: str):
        self.session = client.start_session()
        self.db = self.session.client[db_name]

    def __del__(self):
        self.session.end_session()

    def start_transaction(self):
        self.session.start_transaction()

    def abort_transaction(self):
        self.session.abort_transaction()

    def commit_transaction(self):
        self.session.commit_transaction()

    def save_document(self, collection_name: str, body: dict) -> str:
        try:
            collection = self.db[collection_name]
            inserted_id = collection.insert_one(body, session=self.session).inserted_id
            return str(inserted_id)
        except Exception as e:
            logger.error(e)
            raise MongoDBConnectionException

    def get_all(self, collection_name: str) -> list:
        try:
            collection = self.db[collection_name]
            return MongoDBRepository.convert_cursor_to_list(
                collection.find(session=self.session)
            )
        except Exception as e:
            logger.error(e)
            raise MongoDBConnectionException

    def find_by_id(self, collection_name: str, id: str):
        try:
            collection = self.db[collection_name]
            return collection.find_one({"_id": ObjectId(id)}, session=self.session)
        except Exception as e:
            logger.error(e)
            raise MongoDBConnectionException

    @staticmethod
    def convert_cursor_to_list(cursor: Cursor):
        return [x for x in cursor]
