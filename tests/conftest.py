from unittest import mock

import pytest
from fastapi.testclient import TestClient

from main import get_app


@pytest.fixture(scope="function")
def client():
    return TestClient(get_app())


@pytest.fixture(scope="function")
def mock_get_user():
    with mock.patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name"
    ) as mock_get_user:
        yield mock_get_user


@pytest.fixture(scope="function")
def mock_get_token():
    with mock.patch(
        "app.services.tivit_fake_service.TivitFakeService.get_token"
    ) as mock_get_token:
        yield mock_get_token
