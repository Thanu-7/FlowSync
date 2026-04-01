from pydantic import BaseModel


class DualTrafficData(BaseModel):
    road_A: int
    road_B: int
    pedestrian: bool = False