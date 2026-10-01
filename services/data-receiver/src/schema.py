from pydantic import BaseModel

class SensorData(BaseModel):
    # incoming data are declar as ints due to integer scaling, see docs
    temperature: int
    humidity: int
    pressure: int

class DiagnosticData(BaseModel):
    # diagnostic data from node
    rssi: int
    uptime: int
    reset: str

class ReceiverIn(BaseModel):
    device_id: str # unique id for node sending data
    timestamp: int # unix time stamp
    data: SensorData
    signature: str
    diagnostics: DiagnosticData

class ReceiverResponse(BaseModel):
    status: str