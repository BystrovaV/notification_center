from core.exceptions import MongoDBConnectionException, SesServiceConnectionException
from core.settings import Settings
from domain.email import Email
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

    def __call__(self, email: Email) -> Email:
        # message = json.loads(body.decode("utf-8"))

        self.doc_repository.start_transaction()
        try:
            id = self.doc_repository.save_document(
                self.settings.DB_COLLECTION, email.to_dict()
            )
        except MongoDBConnectionException:
            self.doc_repository.abort_transaction()
            raise Exception

        try:
            message_id = self.email_service.send_email(email.to_address, email.message)
        except SesServiceConnectionException:
            self.doc_repository.abort_transaction()
            raise Exception

        email.id = message_id
        self.doc_repository.commit_transaction()
        return email
