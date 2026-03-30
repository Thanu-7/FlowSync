# In-memory storage (temporary)

traffic_state = {}
signal_state = {}
emergency_state = {
    "active": False,
    "route": [],
    "current_index": 0
}