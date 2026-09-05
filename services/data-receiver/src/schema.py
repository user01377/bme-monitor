from pydantic import BaseModel

class ReceiverIn(BaseModel):
    device_id: str
    timestamp: int
    data: bytes
    signature: bytes

class ReceiverResponse(BaseModel):
    status: str