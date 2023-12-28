import logging

from adapters.aws_services import SESService
from adapters.dead_letter_queue import DeadLetterQueue
from adapters.ses_queue import SesQueue
from core.settings import get_settings
from dependencies.localstack_dependency import get_localstack_ses_client
from dependencies.mongodb_dependencies import get_mongodb_repository
from ports.queue import Queue
from use_case.email_use_case import SaveEmailUseCase


def get_localstack_ses_service() -> SESService:
    base_client = get_localstack_ses_client()
    return SESService(base_client, get_settings())


def save_email_use_case() -> SaveEmailUseCase:
    return SaveEmailUseCase(
        get_localstack_ses_service(), get_mongodb_repository(), get_settings()
    )


def ses_queue() -> SesQueue:
    email_service = save_email_use_case()
    logging.info("create ses")
    return SesQueue(get_settings(), email_service)


def dlq_queue() -> DeadLetterQueue:
    return DeadLetterQueue(get_settings())


def list_queue() -> list[Queue]:
    logging.info("create list")
    return [ses_queue(), dlq_queue()]
