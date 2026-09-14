from pydantic import BaseModel

class AvgDataOut(BaseModel):
    temperature: float
    humidity: float
    pressure: float