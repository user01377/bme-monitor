from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import json
import base64

# PASTE THE PRIVATE KEY GENERATED FROM THE SEED PY HERE
PRIVATE_KEY = bytes.fromhex(
    "PASTE_KEY_FROM_SCRIPT_HERE"
)

payload = {
    "device_id": "test-device",
    "timestamp": 1757070000,
    "data": {
        "temperature": 5.0,
        "humidity": 5.0,
        "pressure": 5.0
    }
}


def main():
    private_key = Ed25519PrivateKey.from_private_bytes(PRIVATE_KEY)

    # Serialize data deterministically so the receiver can
    # reconstruct the exact same bytes for signature verification.
    data_bytes = json.dumps(
        payload["data"],
        separators=(",", ":"),
        sort_keys=True
    ).encode("utf-8")

    message = (
        payload["device_id"].encode("utf-8")
        + payload["timestamp"].to_bytes(8, "big")
        + data_bytes
    )

    signature = private_key.sign(message)

    print("Message:")
    print(message)

    print("\nData JSON:")
    print(data_bytes)

    print("\nSignature (hex):")
    print(signature.hex())

    print("\nSignature (bytes):")
    print(signature)

    print("\nSwagger payload:")
    print(json.dumps({
        "device_id": payload["device_id"],
        "timestamp": payload["timestamp"],
        "data": payload["data"],
        "signature": base64.b64encode(signature).decode(),
    }, indent=2))


if __name__ == "__main__":
    main()