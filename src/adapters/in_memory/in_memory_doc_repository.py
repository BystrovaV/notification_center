import uuid

from ports.repository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self):
        self.collections = {}

    def save_document(self, collection_name: str, body: dict):
        id = uuid.uuid4()
        body["_id"] = id
        self.collections.setdefault(collection_name, []).append(body)
        return id

    def get_all(self, collection_name: str):
        return self.collections.get(collection_name)

    def find_by_id(self, collection_name: str, id):
        if collection := self.collections.get(collection_name):
            for item in collection:
                if item["_id"] == id:
                    return item
