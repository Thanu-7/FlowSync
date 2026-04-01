import time

# In-memory storage

# Stores latest TrafficData per intersection_id
traffic_state = {}

# Stores current signal decision per intersection_id
signal_state = {
    "I1": {
        "current_green": "N",
        "timer": 30,
        "last_switch_time": time.time()
    }
}
# Tracks active emergency vehicle route
emergency_state = {
    "active": False,
    "route": [],
    "current_index": 0,
    "last_update": 0
}

# State for the dual-road signal (road A / road B)
dual_signal_state = {
    "mode": "NORMAL",           # NORMAL | PEDESTRIAN | EMERGENCY
    "current_green": "A",       # A | B | PEDESTRIAN
    "timer": 10,
    "last_switch_time": time.time(),
    "pedestrian_waiting": False,
    "pedestrian_wait_start": None,
    "emergency_road": None,
}