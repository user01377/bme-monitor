from pydantic import BaseModel

class SensorData:
    temperature: float
    humidity: float
    pressure: float

class ReceiverIn(BaseModel):
    device_id: str # unique id for node sending data
    timestamp: int # unix time stamp
    data: SensorData
    signature: str

class ReceiverResponse(BaseModel):
    status: str