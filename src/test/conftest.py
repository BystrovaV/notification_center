import pytest

from core.settings import TestSettings

TestSettings.__test__ = False


@pytest.fixture(scope="session")
def settings():
    return TestSettings()
