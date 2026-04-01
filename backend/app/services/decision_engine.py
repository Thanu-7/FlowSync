from app.services.state import dual_signal_state, emergency_state

MIN_TIME = 10
MAX_TIME = 60


def decide_dual_signal(data):
    A = data.road_A
    B = data.road_B
    pedestrian = data.pedestrian

    # 🚑 1. Emergency override (highest priority)
    if emergency_state["active"]:
        road = emergency_state["road"]

        if road == "A":
            dual_signal_state.update({
                "road_A": "GREEN",
                "road_B": "RED",
                "timer": MAX_TIME,
                "count_A": A,
                "count_B": B,
                "emergency": True,
                "pedestrian": False
            })
        else:
            dual_signal_state.update({
                "road_A": "RED",
                "road_B": "GREEN",
                "timer": MAX_TIME,
                "count_A": A,
                "count_B": B,
                "emergency": True,
                "pedestrian": False
            })

        return dual_signal_state

    # 🚶 2. Pedestrian override
    if pedestrian:
        dual_signal_state.update({
            "road_A": "RED",
            "road_B": "RED",
            "timer": 15,
            "count_A": A,
            "count_B": B,
            "emergency": False,
            "pedestrian": True
        })
        return dual_signal_state

    # 🚗 3. Normal traffic comparison
    if A > B:
        timer = min(MAX_TIME, max(MIN_TIME, A * 2))

        dual_signal_state.update({
            "road_A": "GREEN",
            "road_B": "RED",
            "timer": timer,
            "count_A": A,
            "count_B": B,
            "emergency": False,
            "pedestrian": False
        })

    else:
        timer = min(MAX_TIME, max(MIN_TIME, B * 2))

        dual_signal_state.update({
            "road_A": "RED",
            "road_B": "GREEN",
            "timer": timer,
            "count_A": A,
            "count_B": B,
            "emergency": False,
            "pedestrian": False
        })

    return dual_signal_state