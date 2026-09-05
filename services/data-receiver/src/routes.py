import logging
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

@router.post("/queue-data", response_model=ReceiverResponse)
async def queue_data(payload: ReceiverIn, redis = Depends(get_redis)):
    device = get_device(payload.device_id)

    if not device:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    
    # device authentication logic, for cryptography handshake
    data = base64.b64decode(payload.data)
    signature = base64.b64decode(payload.signature)
    public_key = Ed25519PublicKey.from_public_bytes(device.public_key)

    message = (payload.device_id.encode()) + payload.timestamp.to_bytes(8, "big") + data

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    # push to redis queue
    await redis.lpush("data_queue", payload.model_dump_json())

    return {"status": "queued"}