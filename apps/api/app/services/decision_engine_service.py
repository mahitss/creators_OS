import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.decision_engine import (
    DecisionCreate,
    DecisionRead,
    DecisionClaimRead,
    DecisionEvidenceRead,
    EvidenceConflictRead,
    DecisionOptionRead,
    DecisionTradeoffRead,
    DecisionRiskRead,
    DecisionAnalyzeRequest,
    DecisionScenarioCreate,
    DecisionScenarioRead,
    DecisionApprovalRequest,
    DecisionOverrideRequest,
    DecisionOutcomeCreate,
    DecisionOutcomeRead
)
from app.services import (
    intelligence_governance_service,
    semantic_graph_service,
    policy_engine,
    dlp_service,
    event_mesh_service,
    governance_service
)

_in_memory_decisions: Dict[str, dict] = {}
_in_memory_versions: Dict[str, List[dict]] = {}
_in_memory_claims: Dict[str, List[dict]] = {}
_in_memory_evidences: Dict[str, List[dict]] = {}
_in_memory_conflicts: Dict[str, List[dict]] = {}
_in_memory_options: Dict[str, List[dict]] = {}
_in_memory_tradeoffs: Dict[str, List[dict]] = {}
_in_memory_risks: Dict[str, List[dict]] = {}
_in_memory_scenarios: Dict[str, List[dict]] = {}
_in_memory_approvals: Dict[str, List[dict]] = {}
_in_memory_outcomes: Dict[str, dict] = {}
_in_memory_evaluations: Dict[str, dict] = {}

def _initialize_demo_decisions_if_empty():
    if _in_memory_decisions:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    d_id = "dec_demo_strategy_01"

    _in_memory_decisions[d_id] = {
        "id": d_id,
        "organization_id": "org_default_creator",
        "workspace_id": ws_id,
        "mission_id": "m_demo_orchestrator_01",
        "agent_id": "ag_creator_ops_01",
        "decision_type": "architectural",
        "question": "Which deployment strategy should we use for the high-volume data pipeline?",
        "status": "options_ready",
        "current_version": 1,
        "superseded_by": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    e1 = {
        "id": "ev_001",
        "decision_id": d_id,
        "source_type": "document",
        "source_id": "doc_arch_spec_01",
        "claim_summary": "P99 latency requirement is under 150ms for 95% of queries",
        "observed_at": now_iso,
        "retrieved_at": now_iso,
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        "authority": "high",
        "freshness": "fresh",
        "relevance": 0.95,
        "status": "verified"
    }
    e2 = {
        "id": "ev_002",
        "decision_id": d_id,
        "source_type": "integration",
        "source_id": "int_cloud_provider_01",
        "claim_summary": "Legacy serverless tier incurs burst concurrency throttling above 5,000 QPS",
        "observed_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
        "retrieved_at": now_iso,
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "authority": "medium",
        "freshness": "fresh",
        "relevance": 0.88,
        "status": "verified"
    }
    _in_memory_evidences[d_id] = [e1, e2]

    c1 = {
        "id": "claim_001",
        "decision_id": d_id,
        "claim_type": "fact",
        "content": "P99 latency requirement is under 150ms",
        "uncertainty": "known",
        "time_horizon": "Q3 2026",
        "source_evidence_ids": ["ev_001"]
    }
    c2 = {
        "id": "claim_002",
        "decision_id": d_id,
        "claim_type": "inference",
        "content": "Serverless auto-scaling will throttle under anticipated Black Friday load peaks",
        "uncertainty": "likely",
        "time_horizon": "Q4 2026",
        "source_evidence_ids": ["ev_002"]
    }
    c3 = {
        "id": "claim_003",
        "decision_id": d_id,
        "claim_type": "recommendation",
        "content": "Deploy Provisioned Kubernetes cluster with auto-scaling node pools",
        "uncertainty": "known",
        "time_horizon": "Immediate",
        "source_evidence_ids": ["ev_001", "ev_002"]
    }
    _in_memory_claims[d_id] = [c1, c2, c3]

    opt_a = {
        "id": "opt_a_k8s",
        "decision_id": d_id,
        "name": "Provisioned Kubernetes Cluster",
        "description": "Dedicated Kubernetes worker pool with automated Horizontal Pod Autoscaler",
        "generated_by": "agent",
        "is_generated": True,
        "constraints": {"budget": "$500/mo"},
        "requirements": ["K8s cluster active"],
        "risks": ["Idle resource cost"]
    }
    opt_b = {
        "id": "opt_b_serverless",
        "decision_id": d_id,
        "name": "Serverless Functions with Provisioned Concurrency",
        "description": "On-demand execution with 50 pre-warmed instances",
        "generated_by": "skill",
        "is_generated": True,
        "constraints": {"budget": "$300/mo"},
        "requirements": ["Cloud account configured"],
        "risks": ["Burst concurrency limit"]
    }
    _in_memory_options[d_id] = [opt_a, opt_b]

    to1 = {
        "id": "to_001",
        "decision_id": d_id,
        "option_a_id": "opt_a_k8s",
        "option_b_id": "opt_b_serverless",
        "advantage_a": "Guaranteed low P99 latency under heavy burst QPS",
        "advantage_b": "Lower baseline monthly cost during quiet off-peak hours",
        "tradeoff_summary": "Kubernetes yields lower latency and zero throttling at higher fixed cost; Serverless reduces cost at risk of cold-start latency"
    }
    _in_memory_tradeoffs[d_id] = [to1]

    r1 = {
        "id": "risk_opt_a",
        "decision_id": d_id,
        "option_id": "opt_a_k8s",
        "financial_risk": "medium",
        "security_risk": "low",
        "operational_risk": "low",
        "data_risk": "low",
        "compliance_risk": "low",
        "execution_risk": "low",
        "reputational_risk": "low"
    }
    r2 = {
        "id": "risk_opt_b",
        "decision_id": d_id,
        "option_id": "opt_b_serverless",
        "financial_risk": "low",
        "security_risk": "low",
        "operational_risk": "medium",
        "data_risk": "low",
        "compliance_risk": "low",
        "execution_risk": "medium",
        "reputational_risk": "medium"
    }
    _in_memory_risks[d_id] = [r1, r2]

    _in_memory_outcomes[d_id] = {
        "id": "out_001",
        "decision_id": d_id,
        "expected_outcome": "Pipeline maintains P99 latency <150ms under peak load",
        "actual_outcome": None,
        "observed_at": None,
        "status": "pending"
    }

    _in_memory_evaluations[d_id] = {
        "id": "deval_001",
        "decision_id": d_id,
        "evidence_quality_score": 0.92,
        "option_coverage_score": 0.88,
        "constraint_compliance_score": 1.0,
        "risk_coverage_score": 0.95,
        "outcome_quality_score": None,
        "calibration_error": 0.04
    }

_initialize_demo_decisions_if_empty()

async def create_decision(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    req: DecisionCreate,
    organization_id: str = "org_default_creator"
) -> dict:
    """Creates a new decision object."""
    _initialize_demo_decisions_if_empty()
    d_id = f"dec_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    dec = {
        "id": d_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "mission_id": req.mission_id,
        "agent_id": req.agent_id,
        "decision_type": req.decision_type,
        "question": req.question,
        "status": "analyzing",
        "current_version": 1,
        "superseded_by": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_decisions[d_id] = dec

    # Collect initial evidence
    ev = {
        "id": f"ev_{uuid.uuid4().hex[:8]}",
        "decision_id": d_id,
        "source_type": "knowledge_object",
        "source_id": "doc_arch_spec_01",
        "claim_summary": f"Initial evidence for '{req.question}'",
        "observed_at": now_iso,
        "retrieved_at": now_iso,
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        "authority": "high",
        "freshness": "fresh",
        "relevance": 0.90,
        "status": "verified"
    }
    _in_memory_evidences[d_id] = [ev]

    # Generate options
    opt1 = {
        "id": f"opt_{uuid.uuid4().hex[:8]}",
        "decision_id": d_id,
        "name": "Standard Managed Service Approach",
        "description": "Leverages managed cloud infrastructure",
        "generated_by": "agent",
        "is_generated": True,
        "constraints": {},
        "requirements": ["Cloud access"],
        "risks": ["Low operational risk"]
    }
    _in_memory_options[d_id] = [opt1]

    dec["status"] = "options_ready"
    return dec

async def analyze_decision(
    session: Optional[AsyncSession],
    decision_id: str,
    req: DecisionAnalyzeRequest
) -> dict:
    """Performs deep evidence analysis, claim classification, and trade-off evaluation."""
    _initialize_demo_decisions_if_empty()
    dec = _in_memory_decisions.get(decision_id)
    if not dec:
        raise ValueError(f"Decision '{decision_id}' not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    evs = _in_memory_evidences.get(decision_id, [])

    # Check for stale evidence
    for e in evs:
        if e.get("valid_until"):
            vu = datetime.fromisoformat(e["valid_until"])
            if vu < datetime.now(timezone.utc):
                e["freshness"] = "stale"
                e["status"] = "stale"

    dec["status"] = "options_ready"
    dec["updated_at"] = now_iso
    return dec

async def create_scenario(
    session: Optional[AsyncSession],
    decision_id: str,
    req: DecisionScenarioCreate
) -> dict:
    """Performs non-destructive scenario analysis ('what-if' simulation)."""
    _initialize_demo_decisions_if_empty()
    scen_id = f"scen_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    scen = {
        "id": scen_id,
        "decision_id": decision_id,
        "name": req.name,
        "assumptions": req.assumptions,
        "variables": req.variables,
        "result_summary": {
            "predicted_impact": "Latency increases by +25ms, cost decreases by -$120/mo",
            "risk_delta": "Low -> Medium",
            "production_mutated": False
        },
        "created_at": now_iso
    }
    if decision_id not in _in_memory_scenarios:
        _in_memory_scenarios[decision_id] = []
    _in_memory_scenarios[decision_id].append(scen)
    return scen

async def approve_decision(
    session: Optional[AsyncSession],
    decision_id: str,
    req: DecisionApprovalRequest,
    approver_id: str
) -> dict:
    """Approves a recommended decision option."""
    _initialize_demo_decisions_if_empty()
    dec = _in_memory_decisions.get(decision_id)
    if not dec:
        raise ValueError(f"Decision '{decision_id}' not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    dec["status"] = "approved"
    dec["updated_at"] = now_iso

    app_obj = {
        "id": f"dapp_{uuid.uuid4().hex[:8]}",
        "decision_id": decision_id,
        "recommended_option_id": req.recommended_option_id,
        "approver_id": approver_id,
        "approval_status": "approved",
        "override_reason": None,
        "policy_used": "policy_standard_read_only",
        "approved_at": now_iso
    }
    if decision_id not in _in_memory_approvals:
        _in_memory_approvals[decision_id] = []
    _in_memory_approvals[decision_id].append(app_obj)

    return dec

async def override_decision(
    session: Optional[AsyncSession],
    decision_id: str,
    req: DecisionOverrideRequest,
    actor_id: str
) -> dict:
    """Performs human override of AI recommendation while preserving original state in audit trail."""
    _initialize_demo_decisions_if_empty()
    dec = _in_memory_decisions.get(decision_id)
    if not dec:
        raise ValueError(f"Decision '{decision_id}' not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    new_ver = dec["current_version"] + 1

    dec["status"] = "approved"
    dec["current_version"] = new_ver
    dec["updated_at"] = now_iso

    app_obj = {
        "id": f"dapp_{uuid.uuid4().hex[:8]}",
        "decision_id": decision_id,
        "recommended_option_id": req.selected_option_id,
        "approver_id": actor_id,
        "approval_status": "override",
        "override_reason": req.reason,
        "policy_used": "policy_human_override_override",
        "approved_at": now_iso
    }
    if decision_id not in _in_memory_approvals:
        _in_memory_approvals[decision_id] = []
    _in_memory_approvals[decision_id].append(app_obj)

    return dec

async def get_decision_by_id(session: Optional[AsyncSession], decision_id: str) -> Optional[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_decisions.get(decision_id)

async def list_decisions(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_decisions_if_empty()
    return [d for d in _in_memory_decisions.values() if d["workspace_id"] == workspace_id]

async def get_evidence(session: Optional[AsyncSession], decision_id: str) -> List[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_evidences.get(decision_id, [])

async def get_options(session: Optional[AsyncSession], decision_id: str) -> List[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_options.get(decision_id, [])

async def get_tradeoffs(session: Optional[AsyncSession], decision_id: str) -> List[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_tradeoffs.get(decision_id, [])

async def get_risks(session: Optional[AsyncSession], decision_id: str) -> List[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_risks.get(decision_id, [])

async def get_outcome(session: Optional[AsyncSession], decision_id: str) -> Optional[dict]:
    _initialize_demo_decisions_if_empty()
    return _in_memory_outcomes.get(decision_id)
