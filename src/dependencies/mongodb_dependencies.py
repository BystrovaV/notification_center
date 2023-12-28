from adapters.mongodb import MongoDB, MongoDBRepository
from core.settings import get_settings


class MongoDBDependency:
    def __init__(self):
        self.mongodb = None

    def __call__(self) -> MongoDB:
        settings = get_settings()
        self.mongodb = MongoDB.start(settings) if not self.mongodb else self.mongodb
        return self.mongodb


mongoDB_dependency = MongoDBDependency()


# def get_mongodb_session():
#     mongodb = mongoDB_dependency()
#     with mongodb.client.start_session() as session:
#         with session.start_transaction():
#             yield session
#         logging.info("after session")
# return mongodb.client


def get_mongodb_repository() -> MongoDBRepository:
    # logging.info("create mongodb repository")
    # # with get_mongodb_session() as session:
    # session_generator = get_mongodb_session()
    # try:
    #     session = next(session_generator)
    settings = get_settings()
    #
    #     logging.info("create mongodb repository")
    mongodb = mongoDB_dependency()
    return MongoDBRepository(mongodb.client, settings.DB_NAME)
    # finally:
    #     session_generator.close()
