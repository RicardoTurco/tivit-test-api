from unittest import mock

import pytest
from fastapi.testclient import TestClient

from main import get_app


@pytest.fixture(scope="function")
def client():
    """
    Returns one instance of 'app'.
    """
    return TestClient(get_app())


@pytest.fixture(scope="function")
def mock_get_user():
    """
    Returns one mock of 'get_fake_user_by_name' function.
    """
    with mock.patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name"
    ) as mock_get:
        yield mock_get


@pytest.fixture(scope="function")
def mock_get_token():
    """
    Returns one mock of 'get_token' function.
    """
    with mock.patch(
        "app.services.tivit_fake_service.TivitFakeService.get_token"
    ) as mock_get:
        yield mock_get
