import json

from ports.email_service import EmailService


class SaveEmailUseCase:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def __call__(self, body):
        message = json.loads(body.decode("utf-8"))
        self.email_service.send_email(message["email"], message["msg"])
