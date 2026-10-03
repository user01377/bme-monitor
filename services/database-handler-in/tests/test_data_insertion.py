from src.main import process_payload
from src.models import SensorReads, DiagnosticData

def test_process_payload_inserts_into_database(db_session):
    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
        "data": {
            "temperature": 2500,
            "humidity": 5000,
            "pressure": 101325,
        },
        "diagnostics": {
            "rssi": -55,
            "uptime": 5000,
            "reset": "n/a",
        },
    }

    process_payload(payload, db_session)

    sensor_reading = (
        db_session.query(SensorReads)
        .filter_by(device="test-device")
        .one()
    )

    diagnostic_reading = (
        db_session.query(DiagnosticData)
        .filter_by(device="test-device")
        .one()
    )

    assert sensor_reading.device == "test-device"
    assert sensor_reading.temp == 77.0
    assert sensor_reading.humidity == 50.0
    assert sensor_reading.pressure == 1013.25

    assert diagnostic_reading.device == "test-device"
    assert diagnostic_reading.rssi == -55
    assert diagnostic_reading.uptime == 5000
    assert diagnostic_reading.reset == "n/a"