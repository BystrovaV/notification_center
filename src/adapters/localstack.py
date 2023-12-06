import logging

import boto3
from botocore.client import BaseClient
from botocore.exceptions import NoCredentialsError

from core.settings import Settings
from ports.email_service import EmailService


class LocalStack:
    def __init__(self, session):
        self.session = session

    @classmethod
    def start(cls, settings: Settings):
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )

        return cls(session)


class LocalStackSESService(EmailService):
    def __init__(self, client: BaseClient):
        self.client = client

    def send_email(self, email: str, text: str):
        try:
            self.client.verify_email_identity(
                EmailAddress="user_management@example.org"
            )
            logging.info(f"Email {email} is successfully verifyied")
        except NoCredentialsError as e:
            logging.exception(e)
            # raise LocalStackConnectionException
        except Exception as e:
            logging.exception(e)
            # raise LocalStackConnectionException

        try:
            self.client.send_email(
                Destination={
                    "ToAddresses": [
                        email,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": text,
                        }
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": text,
                    },
                },
                Source="user_management@example.org",
            )
        except Exception as e:
            logging.exception(e)
            # raise LocalStackConnectionException
