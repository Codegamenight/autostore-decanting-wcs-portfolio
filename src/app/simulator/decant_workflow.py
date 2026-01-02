from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional
import time
import uuid

from app.simulator.faults import maybe_raise_fault


class DecantState(str, Enum):
    CREATED = "CREATED"
    TOTE_REQUESTED = "TOTE_REQUESTED"
    TOTE_AT_PORT = "TOTE_AT_PORT"
    ROBOT_DECANTING = "ROBOT_DECANTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


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
    attempt: int = 1
    fault: Optional[str] = None
    fault_code: Optional[str] = None
    operator_message: Optional[str] = None
    recommended_action: Optional[str] = None


def create_decant_task(sku: str, qty: int) -> DecantTask:
    return DecantTask(
        task_id=str(uuid.uuid4()),
        sku=sku,
        qty=qty,
        state=DecantState.CREATED,
        trace=[
            TraceEvent(
                ts=time.time(),
                state=DecantState.CREATED.value,
                message="Task created",
            )
        ],
    )


def run_decant_task(task: DecantTask, force_fault: Optional[str] = None) -> DecantTask:
    def add(state: DecantState, message: str, delay: float = 0.3):
        task.state = state
        task.trace.append(
            TraceEvent(ts=time.time(), state=state.value, message=message)
        )
        time.sleep(delay)

    try:
        add(DecantState.TOTE_REQUESTED, "Requested empty tote at decant port")
        maybe_raise_fault(task.sku, task.attempt, force_fault)

        add(DecantState.TOTE_AT_PORT, "Empty tote arrived at port")
        maybe_raise_fault(task.sku, task.attempt, force_fault)

        add(DecantState.ROBOT_DECANTING, "Robot decanting items into tote")
        maybe_raise_fault(task.sku, task.attempt, force_fault)

        add(DecantState.COMPLETED, "Decant completed; inventory updated")

    except Exception as e:
        msg = str(e)
        task.state = DecantState.FAILED
        task.fault = msg

        if msg.startswith("NO_TOTE_AVAILABLE"):
            task.fault_code = "NO_TOTE_AVAILABLE"
            task.operator_message = "No empty tote available at decant port."
            task.recommended_action = "Check inbound buffer/replenishment and retry."
        elif msg.startswith("ROBOT_PICK_FAILED"):
            task.fault_code = "ROBOT_PICK_FAILED"
            task.operator_message = "Robot failed during pick/decant operation."
            task.recommended_action = "Check robot status, clear fault, then retry."
        else:
            task.fault_code = "UNKNOWN"
            task.operator_message = "Unhandled fault during decant workflow."
            task.recommended_action = "Review trace and escalate to automation support."

        task.trace.append(
            TraceEvent(
                ts=time.time(),
                state=task.state.value,
                message=f"FAILED: {task.fault_code}",
            )
        )

    return task


def task_to_dict(task: DecantTask) -> Dict:
    return {
        "task_id": task.task_id,
        "sku": task.sku,
        "qty": task.qty,
        "state": task.state.value,
        "attempt": task.attempt,
        "fault": task.fault,
        "fault_code": task.fault_code,
        "operator_message": task.operator_message,
        "recommended_action": task.recommended_action,
        "trace": [asdict(e) for e in task.trace],
    }
