# In-memory storage

dual_signal_state = {
    "road_A": "RED",
    "road_B": "RED",
    "timer": 10,
    "count_A": 0,
    "count_B": 0,
    "emergency": False,
    "pedestrian": False
}

# Emergency state
emergency_state = {
    "active": False,
    "road": None   # "A" or "B"
}