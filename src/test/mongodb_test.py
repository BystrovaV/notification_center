import pytest
from pymongo import MongoClient

from adapters.mongodb import MongoDBRepository

# @pytest.fixture
# def settings():
#     return TestSettings()


@pytest.fixture
def mongodb_client(settings):
    mongo_client = MongoClient(settings.get_mongodb_url())
    yield mongo_client

    mongo_client.drop_database(settings.DB_NAME)


@pytest.fixture
def mongodb_repository(mongodb_client, settings):
    return MongoDBRepository(mongodb_client, settings.DB_NAME)


def test_save(mongodb_repository, settings):
    id = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test1": "Test1"})
    assert id is not None

    obj_id = mongodb_repository.get_find_by_id(settings.DB_COLLECTION, id)
    assert obj_id is not None
    assert obj_id["_id"] == id


def test_get_all(mongodb_repository, settings):
    id1 = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test1": "Test1"})

    id2 = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test2": "Test2"})

    assert id1 is not None
    assert id2 is not None

    objs = mongodb_repository.get_all(settings.DB_COLLECTION)
    assert len(objs) == 2
