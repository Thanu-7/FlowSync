from app.services.state import traffic_state, signal_state, emergency_state, dual_signal_state

MIN_TIME = 10
MAX_TIME = 60

def decide_dual_signal(data):
    A = data.road_A
    B = data.road_B
    pedestrian = data.pedestrian

    # 🚶 Pedestrian priority
    if pedestrian:
        dual_signal_state.update({
            "road_A": "RED",
            "road_B": "RED",
            "pedestrian": "GREEN",
            "timer": 15
        })
        return dual_signal_state

    # 🚗 Compare densities
    if A > B:
        timer = min(MAX_TIME, max(MIN_TIME, A * 2))
        dual_signal_state.update({
            "road_A": "GREEN",
            "road_B": "RED",
            "timer": timer
        })
    else:
        timer = min(MAX_TIME, max(MIN_TIME, B * 2))
        dual_signal_state.update({
            "road_A": "RED",
            "road_B": "GREEN",
            "timer": timer
        })

    return dual_signal_state

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

