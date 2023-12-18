from enum import Enum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"


class Settings(BaseSettings):
    environment: EnvironmentTypes = Field(
        EnvironmentTypes.local, env="NOTIFICATION_ENVIRONMENT"
    )

    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"

    DB_NAME: str = "notifications"
    DB_COLLECTION: str = "emails"

    SES_QUEUE: str = "reset_password"
    SES_SOURCE: str = "user_management@example.org"

    RABBIT_USER: str = "root"
    RABBIT_PASSWORD: str = "1234567"
    RABBIT_HOST: str = "localhost"
    RABBIT_PORT: int = 4566

    MONGO_USER: str = "root"
    MONGO_PASSWORD: str = "example"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017

    def get_localstack_endpoint(self):
        return "http://localhost.localstack.cloud:4566"

    def get_rabbitmq_url(self):
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/%2F"

    def get_mongodb_url(self):
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/%2F"


class TestSettings(Settings):
    DB_NAME: str = "tests"


class LocalSettings(Settings):
    pass


# def get_settings():
# return Settings()
environments = {
    EnvironmentTypes.test: TestSettings,
    EnvironmentTypes.local: LocalSettings,
}


@lru_cache
def get_settings() -> Settings:
    app_env = Settings().environment
    return environments[app_env]()


# settings = get_settings()
