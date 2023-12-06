from adapters.localstack import LocalStackSESService
from dependencies.localstack_dependency import get_localstack_ses_client
from use_case.email_use_case import SaveEmailUseCase


def get_localstack_ses_service() -> LocalStackSESService:
    base_client = get_localstack_ses_client()
    return LocalStackSESService(base_client)


def save_email_use_case():
    email_service = get_localstack_ses_service()
    return SaveEmailUseCase(email_service)
