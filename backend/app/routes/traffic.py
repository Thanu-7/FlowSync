from fastapi import APIRouter
from app.models.traffic_model import TrafficData
from app.services.state import traffic_state
from app.services.decision_engine import decide_signal

router = APIRouter()

@router.post("/")
def update_traffic(data: TrafficData):
    traffic_state[data.intersection_id] = data

    # 🔥 CALL DECISION ENGINE
    decide_signal(data.intersection_id)
    
    print("Traffic State:", traffic_state)
    print("Calling decision engine for:", data.intersection_id)

    return {"message": "Traffic processed and signal updated"}



