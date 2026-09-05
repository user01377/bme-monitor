from pydantic import BaseModel

class ReceiverIn(BaseModel):
    device_id: str
    timestamp: int
    data: str
    signature: str

class ReceiverResponse(BaseModel):
    status: str