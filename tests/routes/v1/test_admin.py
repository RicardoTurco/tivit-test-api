from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.services.tivit_fake_service import TivitFakeService


@pytest.mark.asyncio
async def test_get_admin_data_success(client):
    mock_username = "admin_user"

    mock_admin_data = {
        "admin_data": {
            "message": "Hello, admin!",
            "data": {
                "name": "Admin Master",
                "email": "admin@example.com",
                "reports": [
                    {"id": 1, "title": "Monthly Sales", "status": "Completed"},
                    {"id": 2, "title": "User Activity", "status": "Pending"},
                ],
            },
        }
    }

    with patch(
        "app.services.tivit_fake_service.TivitFakeService.get_data_admin",
        new_callable=AsyncMock,
    ) as mock_get_data_admin:

        mock_get_data_admin.return_value = mock_admin_data
        response = client.get(f"/v1/admin?username={mock_username}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"admin_data": mock_admin_data}

        mock_get_data_admin.assert_called_once_with(mock_username)


@pytest.mark.asyncio
async def test_admin_data_external_user_not_found():
    # When endpoint '/v1/admin?username=<admin>' is called,
    # internally call 'admin_data_external' method passing 'username' as a parameter.
    # Here the method is called with a user unknown (not found).
    with patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name",
        new_callable=AsyncMock,
    ) as mock_get_user:

        mock_get_user.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await TivitFakeService.admin_data_external("unknown_user")

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User admin not found"

        mock_get_user.assert_called_once_with("unknown_user")


@pytest.mark.asyncio
async def test_admin_data_external_user_not_authorized():
    # When endpoint '/v1/admin?username=<admin>' is called,
    # internally call 'admin_data_external' method passing 'username' as a parameter.
    # Here the method is called with a user forbidden (not authorized).
    mock_user_non_admin = {
        "username": "non_admin_user",
        "password": "password123",
        "role": "user",
    }

    with patch(
        "app.repositories.fake_user_repository.FakeUserDb.get_fake_user_by_name",
        new_callable=AsyncMock,
    ) as mock_get_user:

        mock_get_user.return_value = mock_user_non_admin

        with pytest.raises(HTTPException) as exc_info:
            await TivitFakeService.admin_data_external("non_admin_user")

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc_info.value.detail == "User not authorized"

        mock_get_user.assert_called_once_with("non_admin_user")
