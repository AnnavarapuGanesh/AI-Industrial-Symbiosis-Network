from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class WasteEvent(BaseModel):
    raw_text: str
    producer_id: str

class MatchResponse(BaseModel):
    id: int
    timestamp: datetime
    producer_name: str
    consumer_name: str
    waste_type: str
    quantity: float
    unit: str
    distance_km: float
    agreement: Dict[str, Any]
    sustainability_pitch: str

    class Config:
        orm_mode = True
