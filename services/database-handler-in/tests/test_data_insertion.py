from src.main import process_payload
from src.models import SensorReads

def test_process_payload_inserts_into_database(db_session):
    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
        "data": {
            "temperature": 2500,
            "humidity": 5000,
            "pressure": 101325,
        },
    }

    process_payload(payload, db_session)

    reading = (
        db_session.query(SensorReads)
        .filter_by(device="test-device")
        .one()
    )

    assert reading.device == "test-device"
    assert reading.temp == 77.0
    assert reading.humidity == 50.0
    assert reading.pressure == 1013.25