import time
from typing import List, Dict

def run_simulation_for_seconds(seconds: int) -> List[Dict]:
    """
    Stage 0 simulator:
    Emits one heartbeat event per second.
    Later stages will implement decanting workflow events.
    """
    events = []
    start = time.time()

    for i in range(seconds):
        now = time.time()
        events.append({
            "type": "SIM_TICK",
            "tick": i + 1,
            "timestamp": round(now, 3),
            "elapsed_s": round(now - start, 3),
        })
        time.sleep(1)

    return events