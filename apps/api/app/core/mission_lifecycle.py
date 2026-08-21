"""Authoritative Mission Lifecycle State Machine & Transition Guards for Kinetiq."""

from typing import Set, Dict, Optional, Any
from enum import Enum

class MissionStatus(str, Enum):
    DRAFT = "DRAFT"
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class MissionStepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class MissionStepType(str, Enum):
    RETRIEVAL = "retrieval"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    GENERATION = "generation"
    ACTION = "action"

class MissionEventType(str, Enum):
    MISSION_CREATED = "MISSION_CREATED"
    MISSION_QUEUED = "MISSION_QUEUED"
    MISSION_PLANNING = "MISSION_PLANNING"
    PLAN_CREATED = "PLAN_CREATED"
    STEP_STARTED = "STEP_STARTED"
    STEP_COMPLETED = "STEP_COMPLETED"
    STEP_FAILED = "STEP_FAILED"
    MODEL_REQUEST = "MODEL_REQUEST"
    MODEL_RESPONSE = "MODEL_RESPONSE"
    MISSION_PAUSED = "MISSION_PAUSED"
    MISSION_RESUMED = "MISSION_RESUMED"
    MISSION_CANCELLED = "MISSION_CANCELLED"
    MISSION_COMPLETED = "MISSION_COMPLETED"
    MISSION_FAILED = "MISSION_FAILED"

# Failure Taxonomy
class FailureType(str, Enum):
    AUTH_ERROR = "AUTH_ERROR"
    POLICY_DENIED = "POLICY_DENIED"
    MODEL_ERROR = "MODEL_ERROR"
    TOOL_ERROR = "TOOL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    TIMEOUT = "TIMEOUT"
    RATE_LIMIT = "RATE_LIMIT"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

# Permitted State Transitions
VALID_STATE_TRANSITIONS: Dict[str, Set[str]] = {
    MissionStatus.DRAFT.value: {MissionStatus.QUEUED.value, MissionStatus.CANCELLED.value, "active"},
    MissionStatus.QUEUED.value: {MissionStatus.PLANNING.value, MissionStatus.PAUSED.value, MissionStatus.CANCELLED.value, MissionStatus.FAILED.value},
    MissionStatus.PLANNING.value: {MissionStatus.RUNNING.value, MissionStatus.PAUSED.value, MissionStatus.CANCELLED.value, MissionStatus.FAILED.value},
    MissionStatus.RUNNING.value: {MissionStatus.WAITING.value, MissionStatus.PAUSED.value, MissionStatus.COMPLETED.value, MissionStatus.FAILED.value, MissionStatus.CANCELLED.value},
    MissionStatus.WAITING.value: {MissionStatus.RUNNING.value, MissionStatus.PAUSED.value, MissionStatus.CANCELLED.value, MissionStatus.FAILED.value},
    MissionStatus.PAUSED.value: {MissionStatus.QUEUED.value, MissionStatus.RUNNING.value, MissionStatus.CANCELLED.value},
    MissionStatus.COMPLETED.value: set(),
    MissionStatus.FAILED.value: set(),
    MissionStatus.CANCELLED.value: set(),
    # Legacy compatibility mappings
    "active": {MissionStatus.QUEUED.value, MissionStatus.RUNNING.value, MissionStatus.PAUSED.value, MissionStatus.COMPLETED.value, MissionStatus.FAILED.value, MissionStatus.CANCELLED.value, "completed", "archived"},
    "draft": {MissionStatus.QUEUED.value, MissionStatus.DRAFT.value, "active", MissionStatus.CANCELLED.value},
    "completed": set(),
    "archived": set()
}

TERMINAL_STATUSES: Set[str] = {
    MissionStatus.COMPLETED.value,
    MissionStatus.FAILED.value,
    MissionStatus.CANCELLED.value,
    "completed",
    "archived"
}

class InvalidMissionStateTransitionError(ValueError):
    def __init__(self, current_status: str, target_status: str, mission_id: Optional[str] = None):
        msg = f"Invalid mission state transition from '{current_status}' to '{target_status}'"
        if mission_id:
            msg += f" for mission {mission_id}"
        super().__init__(msg)
        self.current_status = current_status
        self.target_status = target_status
        self.mission_id = mission_id

class MissionExecutionError(Exception):
    def __init__(self, failure_type: FailureType, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.failure_type = failure_type
        self.message = message
        self.details = details or {}

def normalize_status(status: str) -> str:
    """Normalizes status strings to standard uppercase enums if recognized."""
    if not status:
        return MissionStatus.DRAFT.value
    upper = status.strip().upper()
    if upper in MissionStatus.__members__:
        return MissionStatus[upper].value
    lower = status.strip().lower()
    if lower in ("active", "draft", "completed", "archived"):
        return lower
    return upper

def validate_status_transition(current_status: str, target_status: str, mission_id: Optional[str] = None) -> None:
    """Validates if transitioning from current_status to target_status is permitted by the state machine."""
    curr_norm = normalize_status(current_status)
    target_norm = normalize_status(target_status)

    if curr_norm == target_norm:
        return  # Idempotent same-state is allowed

    allowed = VALID_STATE_TRANSITIONS.get(curr_norm)
    if allowed is None:
        raise InvalidMissionStateTransitionError(current_status, target_status, mission_id)

    if target_norm not in allowed and target_status not in allowed:
        raise InvalidMissionStateTransitionError(current_status, target_status, mission_id)

def is_terminal_status(status: str) -> bool:
    """Returns True if the status is a terminal execution state."""
    norm = normalize_status(status)
    return norm in TERMINAL_STATUSES
