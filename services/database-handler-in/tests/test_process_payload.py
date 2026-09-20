import pytest

from datetime import datetime, timezone

from src.main import process_payload
from src.models import Status

def test_process_payload(mocker):
    session = mocker.Mock()

    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
        "data": {
            "temperature": 2500,
            "humidity": 5000,
            "pressure": 101325,
        },
    }

    process_payload(payload, session)

    sensor_read = session.add.call_args.args[0]
    
    assert sensor_read.device == "test-device"
    assert sensor_read.temp == 77.0
    assert sensor_read.humidity == 50.0
    assert sensor_read.pressure == 1013.25
    assert sensor_read.status == Status.VALID
    assert sensor_read.timestamp == datetime.fromtimestamp(
        1758312000,
        tz=timezone.utc,
    )

    session.commit.assert_called_once()

def test_process_payload_negative_temperature(mocker):
    session = mocker.Mock()

    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
        "data": {
            # negative 5 degree celcius converts to 23 fahrenheit
            "temperature": -500,
            "humidity": 4500,
            "pressure": 100000,
        },
    }

    process_payload(payload, session)

    sensor_read = session.add.call_args.args[0]

    assert sensor_read.temp == 23.0
    assert sensor_read.humidity == 45.0
    assert sensor_read.pressure == 1000.0

def test_process_payload_missing_data_field(mocker):
    session = mocker.Mock()

    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
    }

    with pytest.raises(KeyError):
        process_payload(payload, session)

    session.add.assert_not_called()
    session.commit.assert_not_called()

def test_process_payload_missing_reading(mocker):
    session = mocker.Mock()

    payload = {
        "device_id": "test-device",
        "timestamp": 1758312000,
        "data": {
            # is missing the temperature field
            "humidity": 4500,
            "pressure": 100000
        },
    }

    with pytest.raises(KeyError):
        process_payload(payload, session)

    session.add.assert_not_called()
    session.commit.assert_not_called()