from fastapi import APIRouter
from app.models.traffic_model import TrafficData
from app.services.state import traffic_state
from app.services.decision_engine import decide_signal
from app.models.traffic_model import DualTrafficData
from app.services.decision_engine import decide_dual_signal
from app.services.state import dual_signal_state

router = APIRouter()

@router.post("/dual")
def dual_traffic(data: DualTrafficData):
    result = decide_dual_signal(data)
    return result


@router.get("/dual")
def get_dual_signal():
    return dual_signal_state

@router.post("/")
def update_traffic(data: TrafficData):
    traffic_state[data.intersection_id] = data

    # 🔥 CALL DECISION ENGINE
    decide_signal(data.intersection_id)
    
    print("Traffic State:", traffic_state)
    print("Calling decision engine for:", data.intersection_id)

    return {"message": "Traffic processed and signal updated"}



