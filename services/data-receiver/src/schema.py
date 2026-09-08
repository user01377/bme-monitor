from pydantic import BaseModel

class ReceiverIn(BaseModel):
    device_id: str # unique id for node sending data
    timestamp: int # unix time stamp
    data: SensorData
    signature: str

class SensorData:
    temperature: float
    humidity: float
    pressure: float

class ReceiverResponse(BaseModel):
    status: str