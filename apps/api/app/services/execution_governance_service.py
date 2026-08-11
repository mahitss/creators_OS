import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service, portfolio_intelligence_service

_in_memory_benefits: Dict[str, dict] = {}
_in_memory_evidences: Dict[str, dict] = {}
_in_memory_milestones: Dict[str, dict] = {}
_in_memory_variances: Dict[str, dict] = {}
_in_memory_gates: Dict[str, dict] = {}
_in_memory_change_requests: Dict[str, dict] = {}
_in_memory_forecasts: Dict[str, dict] = {}

def _initialize_seed_execution_data():
    if _in_memory_benefits:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Benefit
    b1 = {
        "id": "ben_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "portfolio_id": "port_01",
        "program_id": "prog_01",
        "initiative_id": "init_01",
        "outcome_id": "out_01",
        "name": "Security Incident MTTR Reduction",
        "description": "Reduce mean-time-to-remediate security threats from 4.5 hours to 15 minutes.",
        "owner": "usr_secops_lead",
        "status": "measuring",
        "benefit_type": "operational",
        "baseline": 4.5,
        "target": 0.25,
        "current_value": 1.2,
        "unit": "hours",
        "measurement_method": "Automated SIEM alert timestamp diff tracking",
        "target_date": "2026-10-30",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_benefits[b1["id"]] = b1

    # Seed Benefit Evidence
    ev1 = {
        "id": "b_ev_01",
        "benefit_id": b1["id"],
        "source": "Vapor SecOps Audit Log #994",
        "reference": "secops_audit_2026_q3.json",
        "observed_at": now_iso,
        "confidence": 98.5,
        "verification_status": "verified"
    }
    _in_memory_evidences[ev1["id"]] = ev1

    # Seed Milestone
    ms1 = {
        "id": "ms_01",
        "initiative_id": "init_01",
        "name": "Threat Intelligence Fabric Deployment",
        "description": "Deploy real-time automated threat pattern detection across agent nodes.",
        "due_date": "2026-08-31",
        "status": "completed",
        "completion_evidence": "Verification test suite #8812 passed with zero critical CVEs."
    }
    _in_memory_milestones[ms1["id"]] = ms1

    # Seed Variance
    v1 = {
        "id": "ex_var_01",
        "initiative_id": "init_01",
        "variance_type": "schedule",
        "baseline": "Target Completion: August 15, 2026",
        "actual": "Current Progress: 85% Complete",
        "forecast": "Forecast Completion: August 28, 2026",
        "delta": "+13 days timeline slip",
        "severity": "medium"
    }
    _in_memory_variances[v1["id"]] = v1

    # Seed Governance Gate
    g1 = {
        "id": "gate_01",
        "initiative_id": "init_01",
        "gate_type": "security",
        "status": "passed",
        "waiver_actor": None,
        "waiver_reason": None
    }
    _in_memory_gates[g1["id"]] = g1

    # Seed Change Request
    cr1 = {
        "id": "cr_01",
        "initiative_id": "init_01",
        "change_type": "timeline",
        "requested_change": "Extend Phase 2 milestone deadline by 14 days.",
        "reason": "Upstream Google Workspace API rate limits required additional caching layer.",
        "impact_summary": "Pushes final deliverable from Aug 15 to Aug 29. No budget impact.",
        "status": "pending",
        "requester": "usr_exec_01"
    }
    _in_memory_change_requests[cr1["id"]] = cr1

    # Seed Forecast
    f1 = {
        "id": "fc_01",
        "initiative_id": "init_01",
        "forecast_completion_date": "2026-08-29",
        "forecast_cost": 45000.0,
        "forecast_benefit": 180000.0,
        "lower_bound": 150000.0,
        "upper_bound": 220000.0,
        "confidence_pct": 91.2
    }
    _in_memory_forecasts[f1["id"]] = f1

_initialize_seed_execution_data()


class ExecutionGovernanceService:

    @staticmethod
    async def get_execution_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_execution_data()
        benefits = list(_in_memory_benefits.values())
        evidences = list(_in_memory_evidences.values())
        milestones = list(_in_memory_milestones.values())
        variances = list(_in_memory_variances.values())
        gates = list(_in_memory_gates.values())
        change_requests = list(_in_memory_change_requests.values())
        forecasts = list(_in_memory_forecasts.values())

        achieved_count = sum(1 for b in benefits if b["status"] == "achieved")
        achieved_rate = (achieved_count / len(benefits)) * 100.0 if benefits else 0.0

        return {
            "benefitsCount": len(benefits),
            "achievedRatePct": round(achieved_rate, 1),
            "milestonesCount": len(milestones),
            "variancesCount": len(variances),
            "gatesCount": len(gates),
            "changeRequestsCount": len(change_requests),
            "benefits": benefits,
            "evidences": evidences,
            "milestones": milestones,
            "variances": variances,
            "gates": gates,
            "changeRequests": change_requests,
            "forecasts": forecasts,
            "executionHealthScore": 0.94
        }

    @staticmethod
    async def create_benefit(session: Optional[AsyncSession], benefit_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_execution_data()
        b_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        b = {
            "id": b_id,
            "organization_id": org_id,
            "workspace_id": "ws_default",
            "portfolio_id": benefit_data.get("portfolioId"),
            "program_id": benefit_data.get("programId"),
            "initiative_id": benefit_data.get("initiativeId"),
            "outcome_id": benefit_data.get("outcomeId"),
            "name": benefit_data["name"],
            "description": benefit_data["description"],
            "owner": benefit_data["owner"],
            "status": "planned",
            "benefit_type": benefit_data["benefitType"],
            "baseline": benefit_data.get("baseline", 0.0),
            "target": benefit_data.get("target", 100.0),
            "current_value": benefit_data.get("baseline", 0.0),
            "unit": benefit_data.get("unit", "USD"),
            "measurement_method": benefit_data["measurementMethod"],
            "target_date": benefit_data.get("targetDate", "2026-12-31"),
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_benefits[b_id] = b
        return b

    @staticmethod
    async def process_natural_language_execution_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_execution_data()

        # Enforce DLP checks on natural language query
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
                    "subject": "Initiative 01 (Security MTTR)",
                    "benefit_name": "Security Incident MTTR Reduction",
                    "status": "measuring",
                    "baseline": "4.5 hours",
                    "current": "1.2 hours",
                    "target": "0.25 hours (15 mins)",
                    "evidence_verification": "verified"
                }
            ],
            "evidenceJson": {
                "referenced_benefits": ["ben_01"],
                "referenced_evidences": ["b_ev_01"],
                "data_source": "Benefits Realization 2.0"
            },
            "confidencePct": 96.0
        }
