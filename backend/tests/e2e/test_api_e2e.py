import httpx
import pytest

BASE_URL = "http://localhost:8000"

@pytest.mark.anyio
async def test_read_transactions_e2e():
    """
    End-to-end test for the read_transactions API endpoint.
    This test makes a real HTTP request to the running service.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/transactions/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # The database is seeded with 25 entries.
    # The default limit is 100, so we should get all 25.
    assert len(data) == 25
    assert "description" in data[0]
    assert "amount" in data[0]
