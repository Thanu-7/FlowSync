from pydantic import BaseModel

class SignalState(BaseModel):
    intersection_id: str
    current_green: str
    timer: int