from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"

    DB_NAME: str = "notifications"
    DB_COLLECTION: str = "emails"

    SES_QUEUE: str = "reset_password"
    SES_SOURCE: str = "user_management@example.org"

    def get_localstack_endpoint(self):
        return "http://localhost.localstack.cloud:4566"

    def get_rabbitmq_url(self):
        return "amqp://root:1234567@localhost:5672/%2F"

    def get_mongodb_url(self):
        return "mongodb://root:example@localhost:27017/"


class TestSettings(Settings):
    DB_NAME: str = "tests"


def get_settings():
    return Settings()
