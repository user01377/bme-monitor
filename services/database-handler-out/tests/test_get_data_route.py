from fastapi.testclient import TestClient

from src.main import app
from src.models import SensorReads, Status

client = TestClient(app)

def test_get_average_data(seeded_db):

    response = client.get("telemetry/average/")

    assert response.status_code == 200

    data = response.json()

    assert data["temperature"] == 25
    assert data["humidity"] == 50
    assert data["pressure"] == 1010