class Settings:
    AWS_ACCESS_KEY_ID = "test"
    AWS_SECRET_ACCESS_KEY = "test"

    def get_localstack_endpoint(self):
        return "http://localhost.localstack.cloud:4566"

    def get_rabbitmq_url(self):
        return "amqp://root:1234567@localhost:5672/%2F"

    def get_mongodb_url(self):
        return "mongodb://root:example@localhost:27017/"


def get_settings():
    return Settings()
