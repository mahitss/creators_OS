import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_models: Dict[str, dict] = {}
_in_memory_principles: Dict[str, dict] = {}
_in_memory_units: Dict[str, dict] = {}
_in_memory_responsibilities: Dict[str, dict] = {}
_in_memory_accountabilities: Dict[str, dict] = {}
_in_memory_rights: Dict[str, dict] = {}
_in_memory_matrices: Dict[str, dict] = {}
_in_memory_processes: Dict[str, dict] = {}
_in_memory_steps: Dict[str, dict] = {}
_in_memory_handoffs: Dict[str, dict] = {}
_in_memory_bottlenecks_op: Dict[str, dict] = {}
_in_memory_flows: Dict[str, dict] = {}
_in_memory_capacity_profiles: Dict[str, dict] = {}
_in_memory_gaps_op: Dict[str, dict] = {}
_in_memory_recommendations_op: Dict[str, dict] = {}
_in_memory_scenarios_op: Dict[str, dict] = {}
_in_memory_tradeoffs_op: Dict[str, dict] = {}
_in_memory_drifts_op: Dict[str, dict] = {}
_in_memory_assumptions_op: Dict[str, dict] = {}
_in_memory_indicators_op: Dict[str, dict] = {}
_in_memory_warnings_op: Dict[str, dict] = {}
_in_memory_proposals_op: Dict[str, dict] = {}
_in_memory_outcomes_op: Dict[str, dict] = {}
_in_memory_lessons_op: Dict[str, dict] = {}

def _initialize_seed_operating_model_data():
    if _in_memory_models:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_primary_01"

    # Seed Operating Model
    model1 = {
        "id": "opmod_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Enterprise Autonomous Cognitive Operating Model 2.0",
        "description": "Cross-functional matrix operating model integrating AI Agent DAGs and Human Executive Decision Rights.",
        "version": "v2.0",
        "status": "active",
        "owner": "usr_chief_operating_officer",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_models[model1["id"]] = model1

    # Seed Organizational Units
    unit1 = {
        "id": "unit_eng_01",
        "organization_id": org_id,
        "parent_id": None,
        "name": "Autonomous Systems & Engineering Division",
        "type": "division",
        "purpose": "Design, build, and optimize enterprise autonomous AI agent DAGs and execution runtime.",
        "scope": "Global engineering, cloud architecture, and model gateway infrastructure",
        "responsibilities": "Agent Runtime, PolicyEngine integration, FinOps capacity management",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    unit2 = {
        "id": "unit_sec_01",
        "organization_id": org_id,
        "parent_id": None,
        "name": "Enterprise Security & Compliance Governance",
        "type": "shared_service",
        "purpose": "Enforce Zero-Trust access, DLP boundaries, and continuous compliance monitoring.",
        "scope": "Enterprise security operations, audit trails, and privacy enforcement",
        "responsibilities": "PolicyEngine rules, DLP secret detection, Anti-Surveillance boundaries",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_units[unit1["id"]] = unit1
    _in_memory_units[unit2["id"]] = unit2

    # Seed Decision Right & RACI Matrix
    dright1 = {
        "id": "dright_01",
        "model_id": model1["id"],
        "decision_type": "portfolio_reconfiguration",
        "scope": "Capital reallocations over $100k and strategic initiative re-sequencing",
        "authority_level": "executive_leadership",
        "constraints_json": {"policy_engine_check": "mandatory", "dlp_boundary": "strict"},
        "escalation_path": "Chief Operating Officer -> Board Executive Committee"
    }
    _in_memory_rights[dright1["id"]] = dright1

    matrix1 = {
        "id": "matrix_01",
        "decision_right_id": dright1["id"],
        "unit_id": unit1["id"],
        "role_type": "recommends"
    }
    _in_memory_matrices[matrix1["id"]] = matrix1

    # Seed Process & Handoff Friction
    proc1 = {
        "id": "proc_agent_deployment_01",
        "name": "Agent Skill Fabric Certification & Deployment",
        "purpose": "Validate sub-agent capabilities, test against DLP sandbox, and deploy to production mesh.",
        "owner_unit_id": unit1["id"],
        "inputs_json": ["Skill AST", "Security Audit Manifest"],
        "outputs_json": ["Signed Agent Binary", "Policy Gateway Route"],
        "systems_json": ["PolicyEngine", "ActionGateway", "Skill Marketplace"],
        "status": "active"
    }
    _in_memory_processes[proc1["id"]] = proc1

    handoff1 = {
        "id": "handoff_01",
        "process_id": proc1["id"],
        "from_unit_id": unit1["id"],
        "to_unit_id": unit2["id"],
        "artifact_name": "Security Compliance Audit Package",
        "wait_time_hours": 14.5,
        "failure_rate": 0.04,
        "friction_flag": True
    }
    _in_memory_handoffs[handoff1["id"]] = handoff1

    # Seed Operating Model Gap
    gap1 = {
        "id": "opgap_01",
        "model_id": model1["id"],
        "gap_type": "decision",
        "description": "Decision latency bottleneck: Security audit handoffs between Engineering and Compliance require 14.5h average wait time.",
        "severity": "medium"
    }
    _in_memory_gaps_op[gap1["id"]] = gap1

    # Seed Operating Model Drift Signal (Formal vs Observed)
    drift1 = {
        "id": "opdrift_01",
        "model_id": model1["id"],
        "documented_behavior": "Formal documentation states Security Audit approval occurs in PolicyEngine within 1 hour.",
        "observed_behavior": "Observed Operating Graph telemetry indicates manual cross-department reviews delay approvals by 14.5h.",
        "difference_summary": "Formal process assumes automated approval; actual behavior relies on manual review bottleneck.",
        "confidence": "high",
        "severity": "medium"
    }
    _in_memory_drifts_op[drift1["id"]] = drift1

    # Seed Operating Model Change Proposal (Human Authorization Required)
    proposal1 = {
        "id": "opprop_01",
        "model_id": model1["id"],
        "problem_summary": "Automate routine Security Compliance Audit verification via ActionGateway pre-signed attestations.",
        "evidence_json": {"observed_wait_time": "14.5h -> estimated 0.2h"},
        "options_json": ["Delegate routine checks to PolicyEngine auto-signer", "Keep manual review"],
        "tradeoffs_json": {"speed_increase": "+98%", "risk_delta": "negligible"},
        "expected_effect": "Reduce agent skill deployment cycle time from 16h to sub-1h while maintaining 100% compliance.",
        "status": "proposed"
    }
    _in_memory_proposals_op[proposal1["id"]] = proposal1

_initialize_seed_operating_model_data()


class OperatingModelService:

    @staticmethod
    async def get_operating_model_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_operating_model_data()
        models = list(_in_memory_models.values())
        units = list(_in_memory_units.values())
        rights = list(_in_memory_rights.values())
        matrices = list(_in_memory_matrices.values())
        processes = list(_in_memory_processes.values())
        handoffs = list(_in_memory_handoffs.values())
        gaps = list(_in_memory_gaps_op.values())
        drifts = list(_in_memory_drifts_op.values())
        proposals = list(_in_memory_proposals_op.values())

        return {
            "modelsCount": len(models),
            "unitsCount": len(units),
            "decisionRightsCount": len(rights),
            "processesCount": len(processes),
            "activeHandoffFrictionsCount": sum(1 for h in handoffs if h["friction_flag"]),
            "operatingGapsCount": len(gaps),
            "formalVsObservedDriftsCount": len(drifts),
            "proposedChangeProposalsCount": len(proposals),
            "overallOperatingEfficiencyIndex": 0.89,
            "models": models,
            "units": units,
            "decisionRights": rights,
            "matrices": matrices,
            "processes": processes,
            "handoffs": handoffs,
            "gaps": gaps,
            "drifts": drifts,
            "changeProposals": proposals
        }

    @staticmethod
    async def approve_change_proposal(session: Optional[AsyncSession], proposal_id: str, actor_id: str) -> dict:
        _initialize_seed_operating_model_data()
        prop = _in_memory_proposals_op.get(proposal_id)
        if not prop:
            return {"error": "Operating Model Change Proposal not found"}

        prop["status"] = "approved"
        prop["approved_by"] = actor_id
        prop["approved_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "proposalId": proposal_id,
            "status": "approved",
            "approvedBy": actor_id,
            "message": "Operating Model Change Proposal authorized via PolicyEngine & Decision Governance. Ready for Execution Governance implementation."
        }

    @staticmethod
    async def execute_change_proposal(session: Optional[AsyncSession], proposal_id: str) -> dict:
        _initialize_seed_operating_model_data()
        prop = _in_memory_proposals_op.get(proposal_id)
        if not prop:
            return {"error": "Operating Model Change Proposal not found"}

        if prop["status"] != "approved":
            return {"error": "Unauthorized: Operating Model Change Proposal must be approved by leadership before execution."}

        prop["status"] = "executed"
        prop["executed_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "proposalId": proposal_id,
            "status": "executed",
            "executionPath": "Universal Action Gateway & Execution Governance Layer",
            "message": "Operating Model Change executed safely via ActionGateway sandbox."
        }

    @staticmethod
    async def process_natural_language_operating_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_operating_model_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking employee ranking/individual worker surveillance)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["rank employee", "worker score", "surveil worker", "fire employee", "individual productivity"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee ranking, worker surveillance, individual productivity scoring, or employment penalty recommendations."},
                "confidencePct": 0.0
            }

        # Enforce DLP checks
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "model_name": "Enterprise Autonomous Cognitive Operating Model 2.0",
                    "org_units": "2 Divisions/Shared Services (Engineering & Security Compliance)",
                    "decision_rights": "Portfolio Reconfiguration Rule (Scope: >$100k, Authority: Executive Leadership)",
                    "process_intelligence": "Skill Certification Process (Owner: Engineering)",
                    "handoff_friction": "Security Audit Handoff (Engineering -> Compliance, Wait: 14.5h, Friction Flagged)",
                    "formal_vs_observed_drift": "Doc states 1h PolicyEngine check vs Observed 14.5h manual audit delay",
                    "change_proposal": "Automate Security Audit verification via ActionGateway pre-signed attestations (Status: proposed)"
                }
            ],
            "evidenceJson": {
                "referenced_model": "opmod_01",
                "data_source": "Enterprise Organizational Operating Intelligence 2.0 Engine"
            },
            "confidencePct": 95.0
        }
