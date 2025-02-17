from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.services.tivit_fake_service import TivitFakeService


@pytest.mark.asyncio
async def test_get_user_data_success(client):
    mock_username = "user_user"

    mock_user_data = {
        "user_data": {
            "message": "Hello, user!",
            "data": {
                "name": "John Doe",
                "email": "john@example.com",
                "purchases": [
                    {"id": 1, "item": "Laptop", "price": 2500},
                    {"id": 2, "item": "Smartphone", "price": 1200},
                ],
            },
        }
    }

    with patch(
        "app.services.tivit_fake_service.TivitFakeService.get_data_user",
        new_callable=AsyncMock,
    ) as mock_get_user_admin:

        mock_get_user_admin.return_value = mock_user_data
        response = client.get(f"/v1/user?username={mock_username}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"user_data": mock_user_data}

        mock_get_user_admin.assert_called_once_with(mock_username)


@pytest.mark.asyncio
async def test_user_data_external_user_not_found():
    # When endpoint '/v1/user?username=<user>' is called,
    # internally call 'data_external_user_info' method passing 'username',
    # 'role' and 'url_tivit' as a parameter.
    # Here the method is called with a user unknown (not found).
    with patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name",
        new_callable=AsyncMock,
    ) as mock_get_user:

        mock_get_user.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await TivitFakeService.data_external_user_info(
                username="unknown_user",
                not_found_msg="user",
                role="role",
                url_tivit="url_tivit",
            )

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"

        mock_get_user.assert_called_once_with("unknown_user")


@pytest.mark.asyncio
async def test_user_data_external_user_not_authorized():
    # When endpoint '/v1/user?username=<user>' is called, internally
    # call 'data_external_user_info' method passing 'username', 'role'
    # and 'url_tivit' as a parameter. Here the method 'data_external_user_info'
    # is called using a diferent 'role' (not authorized).
    mock_user_non_user = {
        "username": "user",
        "password": "password123",
        "role": "user",
    }

    with patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name",
        new_callable=AsyncMock,
    ) as mock_get_user:

        mock_get_user.return_value = mock_user_non_user

        with pytest.raises(HTTPException) as exc_info:
            await TivitFakeService.data_external_user_info(
                username="non_user_user",
                role="another",
                not_found_msg="user",
                url_tivit="url_tivit",
            )

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "User not authorized"

        mock_get_user.assert_called_once_with("non_user_user")
