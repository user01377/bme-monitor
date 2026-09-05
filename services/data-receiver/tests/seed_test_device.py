from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from src.database import SessionLocal
from src.models import Device


device_id = "test-device"

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()


with SessionLocal() as session:
    device = Device(
        device_id=device_id,
        public_key=public_key.public_bytes_raw(),
    )

    session.add(device)
    session.commit()


print(f"Created device: {device_id}")
print("Private key:", private_key.private_bytes_raw().hex())
print("Public key:", public_key.public_bytes_raw().hex())