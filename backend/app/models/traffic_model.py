from pydantic import BaseModel
from typing import Dict

class TrafficData(BaseModel):
    intersection_id: str
    lanes: Dict[str, int]  # N, S, E, W
    pedestrian: bool

class DualTrafficData(BaseModel):
    road_A: int
    road_B: int
    pedestrian: bool = False