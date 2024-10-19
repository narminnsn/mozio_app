from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_provider():
    response = client.post(
        "/providers/",
        json={
            "name": "Provider 1",
            "email": "provider1@example.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Provider 1"


def test_read_provider():
    response = client.get("/providers/1")  # Assuming ID 1 exists
    assert response.status_code == 200


def test_list_providers():
    response = client.get("/providers/")
    assert response.status_code == 200
