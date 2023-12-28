import pytest
from pymongo import MongoClient

from adapters.mongodb import MongoDBRepository


@pytest.fixture(scope="module")
def mongo_client(settings):
    client = MongoClient(settings.get_mongodb_url())
    yield client
    client.drop_database(settings.DB_NAME)
    client.close()


# @pytest.fixture
# def clean(mongo_client, settings):
#     yield
#     mongo_client.drop_database(settings.DB_NAME)


# @pytest.fixture
# def mongodb_session(settings, mongo_client, clean):
#     with mongo_client.start_session() as session:
#         with session.start_transaction():
#             yield session
#             print("after session")


@pytest.fixture
def mongodb_repository(settings, mongo_client):
    yield MongoDBRepository(mongo_client, settings.DB_NAME)
    print("after rep")


def test_save(settings, mongodb_repository):
    id = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test1": "Test1"})
    assert id is not None

    obj_id = mongodb_repository.find_by_id(settings.DB_COLLECTION, id)
    assert obj_id is not None
    assert str(obj_id["_id"]) == id
    print("before pass")


def test_get_all(mongodb_repository, settings):
    id1 = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test1": "Test1"})

    id2 = mongodb_repository.save_document(settings.DB_COLLECTION, {"Test2": "Test2"})

    assert id1 is not None
    assert id2 is not None

    objs = mongodb_repository.get_all(settings.DB_COLLECTION)
    assert len(objs) == 2
