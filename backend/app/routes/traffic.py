from fastapi import APIRouter
from app.models.traffic_model import TrafficData, DualTrafficData
from app.services.state import traffic_state, dual_signal_state
from app.services.decision_engine import decide_signal, decide_dual_signal

router = APIRouter()

@router.post("/dual")
def update_dual(data: DualTrafficData):
    return decide_dual_signal(data)

@router.get("/dual")
def get_dual_signal():
    return dual_signal_state

@router.post("/")
def update_traffic(data: TrafficData):
    # Update current traffic state for the intersection
    traffic_state[data.intersection_id] = data

    # Trigger decision engine to calculate signal state based on new traffic data
    decision = decide_signal(data.intersection_id)

    return {
        "message": "Traffic processed and signal updated",
        "intersection_id": data.intersection_id,
        "signal": decision
    }
