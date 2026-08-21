"""Authoritative Agent Lifecycle, State Machine & Failure Taxonomy for Kinetiq Agent Runtime V1."""

from enum import Enum
from typing import Set, Dict, Optional, Tuple


class AgentStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"


class AgentRunStatus(str, Enum):
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    WAITING_TOOL = "WAITING_TOOL"
    OBSERVING = "OBSERVING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"


class ToolRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AgentFailureType(str, Enum):
    MODEL_ERROR = "MODEL_ERROR"
    MODEL_TIMEOUT = "MODEL_TIMEOUT"
    MODEL_RATE_LIMIT = "MODEL_RATE_LIMIT"
    TOOL_ERROR = "TOOL_ERROR"
    TOOL_TIMEOUT = "TOOL_TIMEOUT"
    POLICY_DENIED = "POLICY_DENIED"
    AUTH_ERROR = "AUTH_ERROR"
    CONTEXT_ERROR = "CONTEXT_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    TOKEN_LIMIT = "TOKEN_LIMIT"
    RUNTIME_TIMEOUT = "RUNTIME_TIMEOUT"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


class AgentEventType(str, Enum):
    AGENT_RUN_CREATED = "AGENT_RUN_CREATED"
    AGENT_INITIALIZED = "AGENT_INITIALIZED"
    CONTEXT_ASSEMBLED = "CONTEXT_ASSEMBLED"
    MODEL_REQUESTED = "MODEL_REQUESTED"
    MODEL_RESPONDED = "MODEL_RESPONDED"
    TOOL_REQUESTED = "TOOL_REQUESTED"
    TOOL_AUTHORIZED = "TOOL_AUTHORIZED"
    TOOL_DENIED = "TOOL_DENIED"
    TOOL_EXECUTED = "TOOL_EXECUTED"
    OBSERVATION_RECORDED = "OBSERVATION_RECORDED"
    AGENT_STEP_STARTED = "AGENT_STEP_STARTED"
    AGENT_STEP_COMPLETED = "AGENT_STEP_COMPLETED"
    AGENT_PAUSED = "AGENT_PAUSED"
    AGENT_FAILED = "AGENT_FAILED"
    AGENT_COMPLETED = "AGENT_COMPLETED"


class InvalidAgentStateTransitionError(ValueError):
    """Raised when an illegal transition is attempted on an Agent."""
    def __init__(self, current_status: str, target_status: str, agent_id: Optional[str] = None):
        self.current_status = current_status
        self.target_status = target_status
        self.agent_id = agent_id
        msg = f"Invalid agent state transition from '{current_status}' to '{target_status}'"
        if agent_id:
            msg += f" for agent {agent_id}"
        super().__init__(msg)


class InvalidAgentRunStateTransitionError(ValueError):
    """Raised when an illegal transition is attempted on an AgentRun."""
    def __init__(self, current_status: str, target_status: str, run_id: Optional[str] = None):
        self.current_status = current_status
        self.target_status = target_status
        self.run_id = run_id
        msg = f"Invalid agent run state transition from '{current_status}' to '{target_status}'"
        if run_id:
            msg += f" for run {run_id}"
        super().__init__(msg)


class AgentExecutionNotAllowedError(PermissionError):
    """Raised when attempting to execute an agent in a non-executable status (DISABLED or ARCHIVED)."""
    def __init__(self, agent_id: str, status: str):
        self.agent_id = agent_id
        self.status = status
        super().__init__(f"Agent {agent_id} in status '{status}' is not permitted to execute.")


# Valid Agent Status Transitions
_AGENT_TRANSITIONS: Dict[str, Set[str]] = {
    AgentStatus.DRAFT.value: {
        AgentStatus.ACTIVE.value,
        AgentStatus.DISABLED.value,
        AgentStatus.ARCHIVED.value
    },
    AgentStatus.ACTIVE.value: {
        AgentStatus.PAUSED.value,
        AgentStatus.DISABLED.value,
        AgentStatus.ARCHIVED.value
    },
    AgentStatus.PAUSED.value: {
        AgentStatus.ACTIVE.value,
        AgentStatus.DISABLED.value,
        AgentStatus.ARCHIVED.value
    },
    AgentStatus.DISABLED.value: {
        AgentStatus.ACTIVE.value,
        AgentStatus.ARCHIVED.value
    },
    AgentStatus.ARCHIVED.value: {
        AgentStatus.DRAFT.value,
        AgentStatus.ACTIVE.value
    },
}

# Valid AgentRun Status Transitions
_AGENT_RUN_TRANSITIONS: Dict[str, Set[str]] = {
    AgentRunStatus.QUEUED.value: {
        AgentRunStatus.INITIALIZING.value,
        AgentRunStatus.PLANNING.value,
        AgentRunStatus.CANCELLED.value,
        AgentRunStatus.FAILED.value
    },
    AgentRunStatus.INITIALIZING.value: {
        AgentRunStatus.PLANNING.value,
        AgentRunStatus.EXECUTING.value,
        AgentRunStatus.CANCELLED.value,
        AgentRunStatus.FAILED.value
    },
    AgentRunStatus.PLANNING.value: {
        AgentRunStatus.EXECUTING.value,
        AgentRunStatus.WAITING_TOOL.value,
        AgentRunStatus.CANCELLED.value,
        AgentRunStatus.FAILED.value,
        AgentRunStatus.COMPLETED.value
    },
    AgentRunStatus.EXECUTING.value: {
        AgentRunStatus.WAITING_TOOL.value,
        AgentRunStatus.OBSERVING.value,
        AgentRunStatus.COMPLETED.value,
        AgentRunStatus.FAILED.value,
        AgentRunStatus.CANCELLED.value,
        AgentRunStatus.TIMED_OUT.value
    },
    AgentRunStatus.WAITING_TOOL.value: {
        AgentRunStatus.OBSERVING.value,
        AgentRunStatus.EXECUTING.value,
        AgentRunStatus.FAILED.value,
        AgentRunStatus.CANCELLED.value,
        AgentRunStatus.TIMED_OUT.value
    },
    AgentRunStatus.OBSERVING.value: {
        AgentRunStatus.EXECUTING.value,
        AgentRunStatus.COMPLETED.value,
        AgentRunStatus.FAILED.value,
        AgentRunStatus.CANCELLED.value
    },
    # Terminal States
    AgentRunStatus.COMPLETED.value: set(),
    AgentRunStatus.FAILED.value: set(),
    AgentRunStatus.CANCELLED.value: set(),
    AgentRunStatus.TIMED_OUT.value: set(),
}

RETRYABLE_AGENT_FAILURES: Set[AgentFailureType] = {
    AgentFailureType.MODEL_TIMEOUT,
    AgentFailureType.MODEL_RATE_LIMIT,
    AgentFailureType.TOOL_TIMEOUT,
    AgentFailureType.MODEL_ERROR,
}


def validate_agent_status_transition(current_status: str, target_status: str, agent_id: Optional[str] = None) -> bool:
    """Validates that a transition from current_status to target_status is permitted for an Agent."""
    c_norm = (current_status or "").upper()
    t_norm = (target_status or "").upper()

    if c_norm == t_norm:
        return True

    allowed = _AGENT_TRANSITIONS.get(c_norm, set())
    if t_norm not in allowed:
        raise InvalidAgentStateTransitionError(c_norm, t_norm, agent_id)
    return True


def validate_agent_run_status_transition(current_status: str, target_status: str, run_id: Optional[str] = None) -> bool:
    """Validates that a transition from current_status to target_status is permitted for an AgentRun."""
    c_norm = (current_status or "").upper()
    t_norm = (target_status or "").upper()

    if c_norm == t_norm:
        return True

    allowed = _AGENT_RUN_TRANSITIONS.get(c_norm, set())
    if t_norm not in allowed:
        raise InvalidAgentRunStateTransitionError(c_norm, t_norm, run_id)
    return True


def validate_agent_executable(agent_id: str, status: str) -> None:
    """Verifies that an agent is in an executable status. Raises AgentExecutionNotAllowedError if DISABLED or ARCHIVED."""
    s_norm = (status or "").upper()
    if s_norm in [AgentStatus.DISABLED.value, AgentStatus.ARCHIVED.value]:
        raise AgentExecutionNotAllowedError(agent_id, s_norm)


def is_retryable_agent_failure(failure_type: str) -> bool:
    """Determines whether a given failure classification is eligible for exponential backoff retry."""
    try:
        f_enum = AgentFailureType(failure_type)
        return f_enum in RETRYABLE_AGENT_FAILURES
    except Exception:
        return False
