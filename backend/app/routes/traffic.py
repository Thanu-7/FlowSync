from fastapi import APIRouter
from app.models.traffic_model import DualTrafficData
from app.services.decision_engine import decide_dual_signal
from app.services.state import dual_signal_state, emergency_state

router = APIRouter()


# 🚗 Main dual traffic API
@router.post("/dual")
def dual_traffic(data: DualTrafficData):
    print("Received:", data)
    result = decide_dual_signal(data)
    return result


# 📊 Get current signal state
@router.get("/dual")
def get_dual_signal():
    return dual_signal_state


# Emergency trigger
@router.post("/emergency")
def trigger_emergency(data: dict):
    print("🚑 Emergency Triggered:", data)   
    emergency_state["active"] = True
    emergency_state["road"] = data.get("road")
    return {"message": "Emergency activated"}


# Clear emergency
@router.post("/clear")
def clear_emergency():
    emergency_state["active"] = False
    emergency_state["road"] = None
    return {"message": "Emergency cleared"}
