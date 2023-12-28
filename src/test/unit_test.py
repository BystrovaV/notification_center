import dataclasses
from unittest.mock import Mock

import pytest
from pydantic_core import ValidationError

from adapters.controller import EmailInput
from adapters.in_memory.in_memory_doc_repository import InMemoryDocumentRepository
from domain.email import Email
from use_case.email_use_case import SaveEmailUseCase

# @pytest.fixture
# def settings():
#     return TestSettings()


@pytest.fixture
def doc_repository():
    return InMemoryDocumentRepository()


@pytest.fixture
def save_email_use_case(doc_repository, settings):
    mock = Mock()
    use_case = SaveEmailUseCase(mock, doc_repository, settings)
    mock.send_email.return_value = {"email": "test"}
    return use_case


def test_doc_repository(doc_repository):
    body = {"email": "test1"}

    id = doc_repository.save_document("test", body)
    assert id is not None

    elem = doc_repository.find_by_id("test", id)
    assert elem is not None
    assert elem["email"] == body["email"]


def test_save_email_use_case(save_email_use_case, doc_repository, settings):
    save_email_use_case(
        Email(to_address="test@example.com", subject="test", message="test")
    )

    items = doc_repository.get_all(settings.DB_COLLECTION)
    assert len(items) == 1
    assert items[0]["to_address"] == "test@example.com"


def test_email_input():
    assert (
        EmailInput(to_address="test@example.com", subject="test", message="test")
        is not None
    )

    with pytest.raises(ValidationError):
        EmailInput(to_address="testexample.com", subject="test", message="test")

    dict = {"to_address": "test@example.com", "subject": "test", "message": "test"}

    assert EmailInput(**dict) is not None


def test_email_input_to_entity():
    dict = {"to_address": "test@example.com", "subject": "test", "message": "test"}

    emailInput = EmailInput(**dict)
    email = emailInput.to_entity()

    assert isinstance(email, Email)
    assert email.to_address == emailInput.to_address
    assert email.subject == emailInput.subject
    assert email.message == emailInput.message

    dict["id"] = None
    assert dataclasses.asdict(email) == dict
    assert email.to_dict() == dict
