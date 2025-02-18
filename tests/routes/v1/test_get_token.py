import pytest
from fastapi import status
from unittest.mock import patch

from app.schemas.token import TokenCredentials


@pytest.mark.asyncio
async def test_get_token_success(client, mock_get_token):
    mock_token_credentials = {"username": "test_user", "password": "test_password"}

    mock_token_data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer",
    }

    mock_get_token.return_value = mock_token_data
    response = client.post("/v1/get-token", json=mock_token_credentials)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer",
    }

    mock_get_token.assert_called_once_with(TokenCredentials(**mock_token_credentials))


@pytest.mark.asyncio
async def test_get_token_user_not_found(client):
    response = client.post(
        "/v1/get-token",
        json={"username": "nonexistent_user", "password": "wrong_password"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert any(
        item in response.json()["detail"]
        for item in ["User admin not found", "User not found"]
    )


@pytest.mark.asyncio
async def test_get_token_wrong_password(client, mock_get_user):
    mock_get_user.return_value = {
        "username": "existing_user",
        "password": "correct_password",
    }

    response = client.post(
        "/v1/get-token",
        json={"username": "existent_user", "password": "wrong_password"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Wrong password" in response.json()["detail"]


@pytest.mark.asyncio
@patch("app.services.tivit_fake_service.requests.post")
async def test_get_token_missing_access_token(
    mock_requests_post, client, mock_get_user
):
    mock_token_credentials = {"username": "test_user", "password": "test_password"}

    mock_user = {"username": "test_user", "password": "test_password", "role": "user"}
    mock_get_user.return_value = mock_user

    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {}

    response = client.post("/v1/get-token", json=mock_token_credentials)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Token not found in response" in response.json()["detail"]

    mock_requests_post.assert_called_once()
