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
async def test_admin_data_external_user_not_found(mock_get_user):
    # When endpoint '/v1/admin?username=<admin>' is called,
    # internally call 'data_external_user_info' method passing 'username',
    # 'not_found_msg', role' and 'url_tivit' as a parameter.
    # Here the method is called with a user unknown (not found).
    mock_get_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await TivitFakeService.data_external_user_info(
            username="unknown_user",
            not_found_msg="admin",
            role="role",
            url_tivit="url_tivit",
        )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User admin not found"

    mock_get_user.assert_called_once_with("unknown_user")


@pytest.mark.asyncio
async def test_admin_data_external_user_not_authorized(mock_get_user):
    # When endpoint '/v1/admin?username=<admin>' is called, internally
    # call 'data_external_user_info' method passing 'username', 'role', 'not_found_msg',
    # and 'url_tivit' as a parameter. Here the method 'data_external_user_info'
    # is called using a diferent 'role' (not authorized).
    mock_user_non_admin = {
        "username": "admin",
        "password": "password123",
        "role": "user",
    }

    mock_get_user.return_value = mock_user_non_admin

    with pytest.raises(HTTPException) as exc_info:
        await TivitFakeService.data_external_user_info(
            username="non_admin_user",
            role="another",
            not_found_msg="admin",
            url_tivit="url_tivit",
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "User not authorized"

    mock_get_user.assert_called_once_with("non_admin_user")
