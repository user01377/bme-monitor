import base64

from src.routes import create_message
from src.schema import SensorData
from src.models import Device

def test_queue_data_success(client, db_session, test_device, redis_mock, mocker):
    device, private_key = test_device

    def get_test_device(device_id):
        with db_session() as session:
            return session.get(Device, device_id)

    mocker.patch(
        "src.routes.get_device",
        side_effect=get_test_device,
    )

    data = SensorData (
        temperature=5,
        humidity=5,
        pressure=5
    )

    message = create_message(
        device.device_id,
        1757070000,
        data
    )

    signature = private_key.sign(message)
    encoded_signature = base64.b64encode(signature).decode()

    payload = {
        "device_id": device.device_id,
        "timestamp": 1757070000,
        "data": {
            "temperature": 5,
            "humidity": 5,
            "pressure": 5,
        },
        "signature": encoded_signature,
    }

    response = client.post("/queue-data", json=payload)    

    assert response.status_code == 200
    assert response.json() == {"status": "queued"}

    redis_mock.lpush.assert_awaited_once()

def test_invalid_signature_data(client, db_session, redis_mock, test_device, mocker):
    device, private_key = test_device

    def get_test_device(device_id):
        with db_session() as session:
            return session.get(Device, device_id)

    mocker.patch(
        "src.routes.get_device",
        side_effect=get_test_device,
    )

    data = SensorData (
        temperature=5,
        humidity=5,
        pressure=5
    )

    message = create_message(
        device.device_id,
        1757070000,
        data
    )

    signature = private_key.sign(message)
    encoded_signature = base64.b64encode(signature).decode()

    payload = {
        "device_id": device.device_id,
        "timestamp": 1757070000,
        "data": {
            "temperature": 100,
            "humidity": 12983,
            "pressure": 12321,
        },
        "signature": encoded_signature,
    }

    response = client.post("/queue-data", json=payload)    

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication failed."}