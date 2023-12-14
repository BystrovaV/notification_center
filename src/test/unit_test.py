import json
from unittest.mock import Mock

import pytest

from adapters.in_memory.in_memory_doc_repository import InMemoryDocumentRepository
from use_case.email_use_case import SaveEmailUseCase

# @pytest.fixture
# def settings():
#     return TestSettings()


@pytest.fixture
def doc_repository():
    return InMemoryDocumentRepository()


@pytest.fixture
def save_email_use_case(doc_repository):
    mock = Mock()
    use_case = SaveEmailUseCase(mock, doc_repository)
    mock.send_email.return_value = {"email": "test"}
    return use_case


def test_doc_repository(doc_repository):
    body = {"email": "test1"}

    id = doc_repository.save_document("test", body)
    assert id is not None

    elem = doc_repository.get_find_by_id("test", id)
    assert elem is not None
    assert elem["email"] == body["email"]


def test_save_email_use_case(save_email_use_case, doc_repository, settings):
    save_email_use_case(json.dumps({"email": "test", "msg": "test"}).encode("utf-8"))

    items = doc_repository.get_all(settings.DB_COLLECTION)
    assert len(items) == 1
    assert items[0]["email"] == "test"
