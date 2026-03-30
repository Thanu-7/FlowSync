from pydantic import BaseModel
from typing import List

class GPSData(BaseModel):
    vehicle_type: str  # ambulance
    route: List[str]
    current_index: int