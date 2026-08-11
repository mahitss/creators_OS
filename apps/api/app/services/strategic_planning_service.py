import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service, decision_engine_service

_in_memory_plans: Dict[str, dict] = {}
_in_memory_objectives: Dict[str, dict] = {}
_in_memory_initiatives: Dict[str, dict] = {}
_in_memory_assumptions: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}
_in_memory_alerts: Dict[str, dict] = {}

def _initialize_seed_strategic_planning_data():
    if _in_memory_plans:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Plan
    p1 = {
        "id": "plan_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "2026 Strategic Growth & Enterprise Expansion",
        "description": "Expand enterprise market share and achieve SOC2 & ISO security certifications.",
        "owner": "usr_exec_01",
        "status": "active",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "version": 1,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_plans[p1["id"]] = p1

    # Seed Objective
    o1 = {
        "id": "obj_01",
        "plan_id": p1["id"],
        "name": "Enterprise Security & Compliance Readiness",
        "description": "Achieve zero-trust security architecture and SOC2 Type II compliance.",
        "priority": "critical",
        "owner": "team_security",
        "status": "active",
        "target": "100% Audit Controls Passed",
        "current_state": "85% Controls Passed",
        "deadline": "2026-09-30"
    }
    _in_memory_objectives[o1["id"]] = o1

    # Seed Initiative
    i1 = {
        "id": "init_01",
        "objective_id": o1["id"],
        "name": "Agent Threat Fabric Deployment",
        "description": "Deploy Zero-Trust runtime policy engine across agent mesh.",
        "owner": "agent_secops_lead",
        "status": "active",
        "priority": "critical",
        "expected_outcome": "Zero unauthorized agent data egress incidents.",
        "estimated_cost": 150000.0,
        "estimated_duration": "4 months"
    }
    _in_memory_initiatives[i1["id"]] = i1

    # Seed Assumption
    a1 = {
        "id": "ass_01",
        "plan_id": p1["id"],
        "statement": "Enterprise customer demand for AI agent governance will double in Q3.",
        "source": "Gartner Market Intelligence Brief 2026",
        "confidence": "high",
        "assumption_type": "market",
        "validity": "valid",
        "created_at": now_iso,
        "verified_at": now_iso,
        "expires_at": "2026-12-31T23:59:59Z"
    }
    _in_memory_assumptions[a1["id"]] = a1

    # Seed Recommendation with Alternatives & Reversibility
    rec1 = {
        "id": "rec_01",
        "plan_id": p1["id"],
        "recommendation": "Accelerate Agent Skill Fabric certification to unblock revenue initiatives.",
        "evidence_json": {"blocked_initiatives_count": 2, "revenue_impact": "$1.2M MRR"},
        "alternatives_json": [
            {
                "option": "Option A: Full Acceleration",
                "description": "Reallocate 2 engineering pods to Skill Fabric verification.",
                "reversibility": "partially_reversible",
                "cost_estimate": "$80k"
            },
            {
                "option": "Option B: Phased Rollout",
                "description": "Certify top 5 high-demand skills first.",
                "reversibility": "reversible",
                "cost_estimate": "$30k"
            },
            {
                "option": "Option C: Status Quo",
                "description": "Maintain existing certification queue cadence.",
                "reversibility": "reversible",
                "cost_estimate": "$0"
            }
        ],
        "tradeoffs_json": {
            "speed": "High",
            "cost": "Medium",
            "risk": "Low",
            "reversibility": "reversible"
        },
        "risks_json": ["Temporary delay in non-critical internal tool refactoring"],
        "assumptions_json": ["Customer contract timelines remain unchanged"],
        "confidence_pct": 92.0
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    # Seed Drift Signal
    d1 = {
        "id": "drift_01",
        "plan_id": p1["id"],
        "drift_type": "execution",
        "signal_summary": "Skill Fabric integration delayed by 1.5 weeks due to API dependency.",
        "evidence_json": {"lag_days": 10, "target_deadline": "2026-09-30"},
        "status": "active",
        "created_at": now_iso
    }
    _in_memory_drifts[d1["id"]] = d1

_initialize_seed_strategic_planning_data()


class StrategicPlanningService:

    @staticmethod
    async def get_strategy_overview(session: Optional[AsyncSession], plan_id: str = "plan_01") -> dict:
        _initialize_seed_strategic_planning_data()
        plan = _in_memory_plans.get(plan_id, list(_in_memory_plans.values())[0])
        objectives = list(_in_memory_objectives.values())
        initiatives = list(_in_memory_initiatives.values())
        assumptions = list(_in_memory_assumptions.values())
        recommendations = list(_in_memory_recommendations.values())
        drifts = list(_in_memory_drifts.values())

        return {
            "plan": plan,
            "objectivesCount": len(objectives),
            "initiativesCount": len(initiatives),
            "assumptionsCount": len(assumptions),
            "strategyDriftCount": len(drifts),
            "objectives": objectives,
            "initiatives": initiatives,
            "assumptions": assumptions,
            "recommendations": recommendations,
            "drifts": drifts,
            "strategyHealthScore": 0.94
        }

    @staticmethod
    async def create_plan(session: Optional[AsyncSession], plan_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_strategic_planning_data()
        p_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        p = {
            "id": p_id,
            "organization_id": org_id,
            "workspace_id": plan_data.get("workspaceId", "ws_default"),
            "name": plan_data["name"],
            "description": plan_data["description"],
            "owner": plan_data["owner"],
            "status": "draft",
            "start_date": plan_data["startDate"],
            "end_date": plan_data["endDate"],
            "version": 1,
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_plans[p_id] = p
        return p

    @staticmethod
    async def verify_assumption(session: Optional[AsyncSession], assumption_id: str) -> dict:
        _initialize_seed_strategic_planning_data()
        a = _in_memory_assumptions.get(assumption_id)
        if not a:
            raise ValueError("Assumption not found")
        now_iso = datetime.now(timezone.utc).isoformat()
        a["validity"] = "valid"
        a["verified_at"] = now_iso
        return a

    @staticmethod
    async def process_natural_language_strategy_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_strategic_planning_data()

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
                    "subject": "Enterprise Security & Compliance Readiness",
                    "status": "at_risk",
                    "reason": "Integration delay in Skill Fabric certification queue",
                    "recommended_action": "Review Option B Phased Skill Rollout"
                }
            ],
            "evidenceJson": {
                "referenced_objectives": ["obj_01"],
                "referenced_recommendations": ["rec_01"],
                "data_source": "Strategic Planning Intelligence 2.0"
            },
            "confidencePct": 94.2
        }
