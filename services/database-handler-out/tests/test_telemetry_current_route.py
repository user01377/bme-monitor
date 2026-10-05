from fastapi.testclient import TestClient

from src.main import app
from src.models import SensorReads, Status

client = TestClient(app)

def test_current_valid(seeded_db):
    response = client.get("/telemetry/current", params={"device_id": "test-device"})
    
    body = response.json()

    assert response.status_code == 200

    assert body["temperature"] == 20
    assert body["humidity"] == 40
    assert body["pressure"] == 1000

def test_current_invalid_device(seeded_db):
    response = client.get("/telemetry/current", params={"device_id": "bad-device"})
    
    body = response.json()

    assert response.status_code == 404
    assert body["detail"] == "Device Not Found"