# In-memory storage (temporary)

traffic_state = {}
signal_state = {}
emergency_state = {
    "active": False,
    "route": [],
    "current_index": 0
}

dual_signal_state = {
    "road_A": "RED",
    "road_B": "RED",
    "timer": 10
}