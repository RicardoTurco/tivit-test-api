import pytest
from unittest.mock import AsyncMock, patch

from app.schemas.token import TokenCredentials


@pytest.mark.asyncio
async def test_get_token_success(client):
    mock_token_credentials = {
        "username": "test_user",
        "password": "test_password"
    }

    mock_token_data = {
        "access_token": "mock_access_token",
        "token_type": "bearer"
    }

    with patch("app.services.tivit_fake_service.TivitFakeService.get_token", new_callable=AsyncMock) as mock_get_token:
        mock_get_token.return_value = mock_token_data
        response = client.post("/v1/get-token", json=mock_token_credentials)

        assert response.status_code == 200
        assert response.json() == {
            "access_token": "mock_access_token",
            "token_type": "bearer"
        }

        mock_get_token.assert_called_once_with(TokenCredentials(**mock_token_credentials))
