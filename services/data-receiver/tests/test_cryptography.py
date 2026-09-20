import base64
import pytest

from fastapi import HTTPException
from src.schema import SensorData

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from src.routes import decode_signature
from src.routes import create_message
from src.routes import verify_signature

def test_decode_signature_valid():
    original = b"test signature"
    encoded = base64.b64encode(original).decode()

    result = decode_signature(encoded)

    assert result == original

def test_decode_signature_invalid():
    with pytest.raises(HTTPException) as exc_info:
        decode_signature("not valid base64!!!")

    assert exc_info.value.status_code == 401

def test_create_message():
    device = "test-device"
    timestamp = 1757070000
    data = SensorData(
        temperature=5,
        humidity=5,
        pressure=5
    )

    message = create_message(device, timestamp, data)

    expected = (
        b"test-device"
        + timestamp.to_bytes(8, "big")
        + b'{"humidity":5,"pressure":5,"temperature":5}'
    )

    assert message == expected

def test_verify_signature_valid():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    message = b"test message"
    signature = private_key.sign(message)

    result = verify_signature(public_key, signature, message)

    assert result is True


def test_verify_signature_invalid():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    message = b"test message"
    signature = private_key.sign(message)

    invalid_message = b"modified message"

    result = verify_signature(public_key, signature, invalid_message)

    assert result is False