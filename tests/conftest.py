import pytest
from fastapi.testclient import TestClient

from main import get_app


@pytest.fixture(scope="function")
def client():
    return TestClient(get_app())
