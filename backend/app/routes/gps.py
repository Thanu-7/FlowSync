from fastapi import APIRouter
from app.models.gps_model import GPSData
from app.services.state import emergency_state

router = APIRouter()

@router.post("/start")
def start_emergency(data: GPSData):
    emergency_state["active"] = True
    emergency_state["route"] = data.route
    emergency_state["current_index"] = data.current_index
    return {"message": "Emergency started"}