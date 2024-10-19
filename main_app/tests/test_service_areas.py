import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_service_area():
    response = client.post(
        "/main_app-areas/",
        json={
            "name": "Service Area 1",
            "price": 10.0,
            "geojson": '{"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}',
            "provider_id": "1",  # Assuming provider with ID 1 exists
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Service Area 1"


def test_read_service_area():
    response = client.get("/main_app-areas/1")  # Assuming ID 1 exists
    assert response.status_code == 200


def test_list_service_areas():
    response = client.get("/main_app-areas/")
    assert response.status_code == 200
