from fastapi.testclient import TestClient

from src.main import app
from src.models import SensorReads, Status

client = TestClient(app)

def test_get_average_data(db_session):
    db_session.add_all([
        SensorReads(
            device="test-device",
            temp=20,
            humidity=40,
            pressure=1000,
            status=Status.VALID,
        ),
        SensorReads(
            device="test-device",
            temp=30,
            humidity=60,
            pressure=1020,
            status=Status.VALID,
        ),
    ])
    db_session.commit()

    response = client.get("telemetry/average/")

    assert response.status_code == 200

    data = response.json()

    assert data["temperature"] == 25
    assert data["humidity"] == 50
    assert data["pressure"] == 1010