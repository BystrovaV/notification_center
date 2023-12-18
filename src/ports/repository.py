from abc import ABC, abstractmethod


class DocumentRepository(ABC):
    @abstractmethod
    def save_document(self, collection_name: str, body: dict):
        pass

    @abstractmethod
    def get_all(self, collection_name: str):
        pass

    @abstractmethod
    def find_by_id(self, collection_name: str, id):
        pass
