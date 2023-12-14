import boto3
import pytest

from adapters.localstack import LocalStackSESService


@pytest.fixture(scope="module")
def boto3_session(settings):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )

    return session


@pytest.fixture(scope="module")
def ses_client(boto3_session, settings):
    return boto3_session.client("ses", endpoint_url=settings.get_localstack_endpoint())


@pytest.fixture
def local_stack_ses_service(ses_client, settings):
    return LocalStackSESService(ses_client, settings)


def test_send_email(local_stack_ses_service):
    message_id = local_stack_ses_service.send_email("test1@example.com", "Test message")
    assert message_id is not None
