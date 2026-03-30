from fastapi import APIRouter
from app.services.state import signal_state

router = APIRouter()

@router.get("/")
def get_signals():
    return signal_state