import json

from core.exceptions import MongoDBConnectionException, SesServiceConnectionException
from core.settings import Settings
from ports.email_service import EmailService
from ports.repository import DocumentRepository


class SaveEmailUseCase:
    def __init__(
        self,
        email_service: EmailService,
        doc_repository: DocumentRepository,
        settings: Settings,
    ):
        self.doc_repository = doc_repository
        self.email_service = email_service
        self.settings = settings

    def __call__(self, body):
        message = json.loads(body.decode("utf-8"))

        try:
            id = self.doc_repository.save_document(self.settings.DB_COLLECTION, message)
        except MongoDBConnectionException:
            raise Exception

        try:
            message_id = self.email_service.send_email(message["email"], message["msg"])
        except SesServiceConnectionException:
            raise Exception

        message["message_id"] = message_id
