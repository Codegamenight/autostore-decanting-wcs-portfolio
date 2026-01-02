from enum import Enum

class FaultCode(str, Enum):
    NO_TOTE_AVAILABLE = "NO_TOTE_AVAILABLE"
    ROBOT_PICK_FAILED = "ROBOT_PICK_FAILED"
