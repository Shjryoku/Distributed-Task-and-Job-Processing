import pytest

@pytest.mark.asyncio
async def test_create_task(client):
    response = await client.post("/tasks/", json={
        "name": "send_email",
        "priority": 1,
        "payload": {"email": "test@test.com"},
        "retry_limit": 3,
        "timeout_seconds": 300
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "send_email"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_create_task_idempotency(client):
    payload = {
        "name": "send_email",
        "priority": 1,
        "payload": {"email": "test@test.com"},
        "idempotency_key": "abc-123",
        "retry_limit": 3,
        "timeout_seconds": 300
    }

    response1 = await client.post("/tasks/", json=payload)
    response2 = await client.post("/tasks/", json=payload)

    assert response1.status_code == 201
    assert response2.status_code == 201
    data1 = response1.json()
    data2 = response2.json()
    assert data1["id"] == data2["id"]

@pytest.mark.asyncio
async def test_get_next_task_empty(client):
    response = await client.get("/tasks/next?worker_id=worker_test&timeout_sec=30")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"