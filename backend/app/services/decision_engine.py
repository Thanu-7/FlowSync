import time
from app.services.state import dual_signal_state, traffic_state, signal_state, emergency_state

MIN_GREEN = 10
MAX_GREEN = 60
PEDESTRIAN_TIME = 60
MAX_WAIT = 60


def decide_dual_signal(data):
    now = time.time()

    A = data.road_A
    B = data.road_B
    pedestrian = data.pedestrian
    emergency = getattr(data, "emergency", None)

    state = dual_signal_state

    elapsed = now - state["last_switch_time"]

    # 🟡 1. HANDLE PEDESTRIAN REQUEST
    if pedestrian and not state["pedestrian_waiting"]:
        state["pedestrian_waiting"] = True
        state["pedestrian_wait_start"] = now

    # 🔴 2. EMERGENCY OVERRIDE (unless pedestrian active)
    if emergency and state["mode"] != "PEDESTRIAN":
        state["mode"] = "EMERGENCY"
        state["current_green"] = emergency
        state["timer"] = MAX_GREEN
        state["last_switch_time"] = now
        state["emergency_road"] = emergency

        return format_output()

    # 🚶 3. PEDESTRIAN MODE
    if state["mode"] == "PEDESTRIAN":
        if elapsed >= PEDESTRIAN_TIME:
            state["mode"] = "NORMAL"
            state["pedestrian_waiting"] = False
            state["pedestrian_wait_start"] = None
            state["last_switch_time"] = now
        else:
            return format_output()

    # ⏳ 4. WAIT FOR TIMER (NORMAL MODE)
    if elapsed < state["timer"] and state["mode"] == "NORMAL":
        return format_output()

    # 🚶 5. CHECK IF PEDESTRIAN SHOULD ACTIVATE
    if state["pedestrian_waiting"]:
        wait_time = now - state["pedestrian_wait_start"]

        if wait_time >= MAX_WAIT or elapsed >= state["timer"]:
            state["mode"] = "PEDESTRIAN"
            state["current_green"] = "PEDESTRIAN"
            state["timer"] = PEDESTRIAN_TIME
            state["last_switch_time"] = now

            return format_output()

    # 🚗 6. NORMAL TRAFFIC SWITCH
    if A > B:
        chosen = "A"
        density = A
    else:
        chosen = "B"
        density = B

    state["mode"] = "NORMAL"
    state["current_green"] = chosen
    state["timer"] = min(MAX_GREEN, max(MIN_GREEN, density * 2))
    state["last_switch_time"] = now

    return format_output()


def format_output():
    state = dual_signal_state

    return {
        "road_A": "GREEN" if state["current_green"] == "A" else "RED",
        "road_B": "GREEN" if state["current_green"] == "B" else "RED",
        "pedestrian": "GREEN" if state["mode"] == "PEDESTRIAN" else "RED",
        "mode": state["mode"],
        "timer": int(state["timer"])
    }


def update_emergency_position():
    if not emergency_state.get("active"):
        return

    current_time = time.time()
    last_update = emergency_state.get("last_update", 0)

    if current_time - last_update >= 10:
        emergency_state["current_index"] += 1
        emergency_state["last_update"] = current_time

        # Check if route is finished
        if emergency_state["current_index"] >= len(emergency_state.get("route", [])):
            emergency_state["active"] = False
            emergency_state["current_index"] = 0


def decide_signal(intersection_id: str):

    if current.get("current_green") == "EMERGENCY":
        return current
    """
    Multi-lane intersection decision engine.
    Priority:
      1. Emergency vehicle -> give green (Overrides EVERYTHING)
      2. Timer locking logic -> hold signals that are actively counting down
      3. Pedestrian -> activate pedestrian phase
      4. Traffic -> choose lane with highest vehicles
    """
    update_emergency_position()

    current_time = time.time()
    current = signal_state.get(intersection_id) or {}
    data = traffic_state.get(intersection_id)

    # Safety check: if no traffic data exists and no existing signal state exists, return {}
    if not data and not current:
        return {}

    # 1. EMERGENCY OVERRIDE (Evaluated first, ignores timer constraints)
    is_emergency = False
    if emergency_state.get("active") and emergency_state.get("route"):
        current_idx = emergency_state.get("current_index", 0)
        route = emergency_state.get("route", [])
        if current_idx < len(route):
            expected_intersection = route[current_idx]
            if str(expected_intersection) == str(intersection_id):
                is_emergency = True
                
                # Green Corridor Pre-activation
                if current_idx + 1 < len(route):
                    next_intersection = str(route[current_idx + 1])
                    next_current = signal_state.get(next_intersection) or {}
                    
                    if next_current.get("current_green") != "EMERGENCY":
                        signal_state[next_intersection] = {
                            "current_green": "EMERGENCY",
                            "timer": MAX_GREEN,
                            "last_switch_time": current_time
                        }

    if is_emergency:
        # Prevent unnecessary reset if already in emergency mode
        if current.get("current_green") == "EMERGENCY":
            return current
            
        decision = {
            "current_green": "EMERGENCY",
            "timer": MAX_GREEN,
            "last_switch_time": current_time
        }
        signal_state[intersection_id] = decision
        return decision

    # 2. TIME-BASED SIGNAL CONTROL (Locking)
    if current:
        last_switch_time = current.get("last_switch_time", 0)
        timer = current.get("timer", 0)
        if current_time - last_switch_time < timer:
            return current

    # If timer expired but no traffic data, maintain current or revert to empty dict
    if not data:
        return current or {}

    # 3. PEDESTRIAN CHECK
    if getattr(data, "pedestrian", False):
        if current.get("current_green") == "PEDESTRIAN":
            return current
            
        decision = {
            "current_green": "PEDESTRIAN",
            "timer": 20,  # Fixed pedestrian crossing time for simplicity
            "last_switch_time": current_time
        }
        signal_state[intersection_id] = decision
        return decision

    # 4. TRAFFIC DENSITY CHECK
    lanes = getattr(data, "lanes", {}) or {}
    if lanes:
        # Find lane with highest vehicle count safely
        best_lane = max(lanes, key=lanes.get)
        max_vehicles = lanes.get(best_lane, 0)

        # PREVENT UNNECESSARY SIGNAL RESET
        if current.get("current_green") == best_lane:
            return current

        # 2 seconds per vehicle, bounded by MIN_GREEN and MAX_GREEN
        duration = max(MIN_GREEN, min(MAX_GREEN, max_vehicles * 2))

        decision = {
            "current_green": best_lane,
            "timer": duration,
            "last_switch_time": current_time
        }
        signal_state[intersection_id] = decision
        return decision

    # Fallback if no valid vehicles and no pedestrians
    if current.get("current_green") == "NONE":
        return current
        
    decision = {
        "current_green": "NONE",
        "timer": MIN_GREEN,
        "last_switch_time": current_time
    }
    signal_state[intersection_id] = decision
    return decision