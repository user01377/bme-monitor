import sys
from src.database import engine
from src.models import Device
from sqlalchemy.orm import Session

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def reg_device(name: str, key: str):

    # validate public key that is passed into script
    try:
        public_key = bytes.fromhex(key)
        Ed25519PublicKey.from_public_bytes(public_key)
    except ValueError:
        print("Error: key must be a valid 32-byte Ed25519 public key.")
        sys.exit(1)

    with Session(engine) as session:
        device = Device(
            device_id=name,
            public_key=public_key
        )

        session.add(device)
        session.commit()

        print(f"Succesfully registered {name} into the database. DEBUG: {public_key} ENTERED")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m scripts.register_device <name> <key>")
        sys.exit(1)
    
    reg_device(sys.argv[1], sys.argv[2])