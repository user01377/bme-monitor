import logging
import json
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from fastapi import APIRouter, HTTPException, Depends
from .schema import ReceiverIn, ReceiverResponse
from .database import get_device
from .redis_client import get_redis

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
def get_health():
    return {"status": "ok"}


def decode_signature(payload_signature) -> bytes:
    """
    Helper function to decode the received payload signature, str -> bytes
    """
    try:
        signature = base64.b64decode(payload_signature)
        return signature
    except ValueError:
        raise HTTPException(status_code=401, detail="Authentication failed.")

def create_message(device_id, timestamp, data) -> bytes:
    """
    Helper function to create the cryptography signature
    signature = device_id + timestamp + json_data
    """

    data_json = json.dumps(data.model_dump(), separators=(",", ":"), sort_keys=True)

    return device_id.encode("utf-8") + timestamp.to_bytes(8, "big") + data_json.encode("utf-8")

def verify_signature(public_key, signature, message) -> bool:
    """
    Helper function for authenticating via cryptography handshake
    """

    try:
        public_key.verify(signature, message)
        return True
    except (InvalidSignature, ValueError):
        return False

@router.post("/queue-data", response_model=ReceiverResponse)
async def queue_data(payload: ReceiverIn, redis = Depends(get_redis)):
    device = get_device(payload.device_id)

    if not device:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    public_key = Ed25519PublicKey.from_public_bytes(device.public_key)
    signature = decode_signature(payload.signature)
    message = create_message(payload.device_id, payload.timestamp, payload.data)

    if not verify_signature(public_key, signature, message):
        raise HTTPException(status_code=401, detail="Authentication failed.")

    # push to redis queue
    await redis.lpush("data_queue", payload.model_dump_json())

    return {"status": "queued"}