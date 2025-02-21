from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_external_health_check_success(client):
    """
    Test: test_external_health_check_success.
    """
    mock_external_app_result = {"external_application": True}

    with patch(
        "app.services.tivit_fake_service.TivitFakeService.external_health_check",
        new_callable=AsyncMock,
    ) as mock_external_health_check:

        mock_external_health_check.return_value = mock_external_app_result
        response = client.get("/v1/external-health-check")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"external_application": True}


@pytest.mark.asyncio
async def test_health_check_success(client):
    """
    Test: test_health_check_success.
    """
    response = client.get("/v1/health-check")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"application": True}
