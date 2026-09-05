from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import json
import base64

# PASTE THE PRIVATE KEY GENERATED FROM THE SEED PY HERE
PRIVATE_KEY = bytes.fromhex(
    "ENTER_KEY_HERE"
)

payload = {
    "device_id": "test-device",
    "timestamp": 1757070000,
    "data": b"hello from test client",
}

def main():
    private_key = Ed25519PrivateKey.from_private_bytes(PRIVATE_KEY)

    message = (
        payload["device_id"].encode()
        + payload["timestamp"].to_bytes(8, "big")
        + payload["data"]
    )

    signature = private_key.sign(message)

    print("Message:")
    print(message)

    print("\nSignature (hex):")
    print(signature.hex())

    print("\nSignature (bytes):")
    print(signature)

    print("\nSwagger payload:")
    print(json.dumps({
        "device_id": payload["device_id"],
        "timestamp": payload["timestamp"],
        "data": base64.b64encode(payload["data"]).decode(),
        "signature": base64.b64encode(signature).decode(),
    }, indent=2))

if __name__ == "__main__":
    main()