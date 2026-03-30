from app.services.state import traffic_state, signal_state, emergency_state

MIN_GREEN = 10
MAX_GREEN = 60


def decide_signal(intersection_id):
    traffic = traffic_state.get(intersection_id)

    if not traffic:
        return

    lanes = traffic.lanes
    pedestrian = traffic.pedestrian

    # 🚑 1. Emergency Priority
    if emergency_state["active"]:
        route = emergency_state["route"]
        current_index = emergency_state["current_index"]

        if current_index < len(route) and route[current_index] == intersection_id:
            signal_state[intersection_id] = {
                "current_green": "EMERGENCY",
                "timer": MAX_GREEN
            }
            return

    # 🚶 2. Pedestrian Priority
    if pedestrian:
        signal_state[intersection_id] = {
            "current_green": "PEDESTRIAN",
            "timer": 20
        }
        return

    # 🚗 3. Traffic Optimization
    max_lane = max(lanes, key=lanes.get)
    vehicle_count = lanes[max_lane]

    green_time = min(MAX_GREEN, max(MIN_GREEN, vehicle_count * 2))

    signal_state[intersection_id] = {
        "current_green": max_lane,
        "timer": green_time
    }

