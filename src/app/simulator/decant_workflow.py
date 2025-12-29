from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List
import time
import uuid

class DecantState(str, Enum):
    CREATED = "CREATED"
    TOTE_REQUESTED = "TOTE_REQUESTED"
    TOTE_AT_PORT = "TOTE_AT_PORT"
    ROBOT_DECANTING = "ROBOT_DECANTING"
    COMPLETED = "COMPLETED"

@dataclass
class TraceEvent:
    ts: float
    state: str
    message: str

@dataclass
class DecantTask:
    task_id: str
    sku: str
    qty: int
    state: DecantState
    trace: List[TraceEvent]

def create_decant_task(sku: str, qty: int) -> DecantTask:
    task_id = str(uuid.uuid4())
    task = DecantTask(
        task_id=task_id,
        sku=sku,
        qty=qty,
        state=DecantState.CREATED,
        trace=[TraceEvent(ts=time.time(), state=DecantState.CREATED, message="Task created")],
    )
    return task

def run_decant_task(task: DecantTask) -> DecantTask:
    def add(state: DecantState, msg: str, sleep_s: float = 0.5):
        task.state = state
        task.trace.append(TraceEvent(ts=time.time(), state=state, message=msg))
        time.sleep(sleep_s)

    add(DecantState.TOTE_REQUESTED, "Requested empty tote at decant port")
    add(DecantState.TOTE_AT_PORT, "Empty tote arrived at port")
    add(DecantState.ROBOT_DECANTING, "Robot decanting items into tote")
    add(DecantState.COMPLETED, "Decant completed; inventory updated")

    return task

def task_to_dict(task: DecantTask) -> Dict:
    return {
        "task_id": task.task_id,
        "sku": task.sku,
        "qty": task.qty,
        "state": task.state.value,
        "trace": [asdict(e) for e in task.trace],
    }