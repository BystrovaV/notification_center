from adapters.aws_services import AWSEngine
from core.settings import get_settings


class LocalStackDependency:
    def __init__(self):
        self.localstack = None

    def __call__(self) -> AWSEngine:
        settings = get_settings()
        self.localstack = (
            AWSEngine.start(settings) if not self.localstack else self.localstack
        )
        return self.localstack


def get_localstack_ses_client():
    settings = get_settings()
    localstack = LocalStackDependency()()

    return localstack.session.client(
        "ses", endpoint_url=settings.get_localstack_endpoint()
    )
