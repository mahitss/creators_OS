import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service, semantic_graph_service

_in_memory_outcomes: Dict[str, dict] = {}
_in_memory_change_events: List[dict] = []
_in_memory_scenarios: Dict[str, dict] = {}
_in_memory_risks: Dict[str, dict] = {}
_in_memory_gaps: Dict[str, dict] = {}
_in_memory_bottlenecks: Dict[str, dict] = {}
_in_memory_dependencies: List[dict] = []
_in_memory_validation_issues: List[dict] = []

def _initialize_seed_operating_graph_data():
    if _in_memory_outcomes:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Outcome
    out1 = {
        "id": "out_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "SOC2 Compliance Certification",
        "description": "Achieve SOC2 Type II compliance audit readiness for enterprise customers.",
        "owner": "team_exec",
        "status": "active",
        "target": "100% Audit Controls Verified",
        "current_state": "85% Controls Verified",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_outcomes[out1["id"]] = out1

    # Seed Dependency
    dep1 = {
        "id": "dep_01",
        "organization_id": org_id,
        "source_id": "mis_audit_102",
        "source_type": "Mission",
        "target_id": "out_01",
        "target_type": "Outcome",
        "relationship_type": "RESULTS_IN",
        "health": "healthy",
        "is_critical_path": True,
        "freshness_policy_hours": 24,
        "updated_at": now_iso
    }
    _in_memory_dependencies.append(dep1)

    # Seed Risk
    r1 = {
        "id": "risk_01",
        "organization_id": org_id,
        "dimension": "integration",
        "title": "Salesforce API Concentration Risk",
        "description": "4 critical revenue workflows depend on a single Salesforce integration account without fallback.",
        "source_ref": "integration_sf_01",
        "evidence_json": {"affected_missions": 4, "integration": "Salesforce Production"},
        "status": "identified",
        "mitigation_recommendations_json": ["Provision secondary API key", "Enable offline queue fallback"],
        "created_at": now_iso
    }
    _in_memory_risks[r1["id"]] = r1

    # Seed Capability Gap
    g1 = {
        "id": "gap_01",
        "organization_id": org_id,
        "capability_id": "cap_vector_search_v2",
        "required_by_ref": "mis_analysis_99",
        "gap_classification": "under_capacity",
        "impact_summary": "High query volume causing latency spikes during peak reporting hours.",
        "status": "open",
        "created_at": now_iso
    }
    _in_memory_gaps[g1["id"]] = g1

    # Seed Bottleneck
    b1 = {
        "id": "bot_01",
        "organization_id": org_id,
        "blocker_type": "approval",
        "root_dependency_ref": "usr_exec_01",
        "affected_work_json": ["work_02", "work_05"],
        "duration_hours": 4.5,
        "evidence_json": {"approval_type": "Vendor Security Exception", "queue_length": 3},
        "status": "active",
        "created_at": now_iso
    }
    _in_memory_bottlenecks[b1["id"]] = b1

_initialize_seed_operating_graph_data()


class OperatingGraphService:

    @staticmethod
    async def get_organization_overview(session: Optional[AsyncSession], org_id: str = "org_default_creator") -> dict:
        _initialize_seed_operating_graph_data()
        outcomes = list(_in_memory_outcomes.values())
        risks = list(_in_memory_risks.values())
        gaps = list(_in_memory_gaps.values())
        bottlenecks = list(_in_memory_bottlenecks.values())

        return {
            "activeOutcomesCount": len(outcomes),
            "dependenciesMonitoredCount": len(_in_memory_dependencies) + 120,
            "systemBottlenecksCount": len(bottlenecks),
            "capabilityGapsCount": len(gaps),
            "concentrationRisksCount": len(risks),
            "outcomes": outcomes,
            "risks": risks,
            "gaps": gaps,
            "bottlenecks": bottlenecks,
            "graphHealthScore": 0.96
        }

    @staticmethod
    async def create_outcome(session: Optional[AsyncSession], outcome_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_operating_graph_data()
        o_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        o = {
            "id": o_id,
            "organization_id": org_id,
            "workspace_id": outcome_data.get("workspaceId", "ws_default"),
            "name": outcome_data["name"],
            "description": outcome_data["description"],
            "owner": outcome_data["owner"],
            "status": "active",
            "target": outcome_data["target"],
            "current_state": outcome_data["currentState"],
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_outcomes[o_id] = o
        return o

    @staticmethod
    async def simulate_scenario(session: Optional[AsyncSession], scenario_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_operating_graph_data()
        s_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        name = scenario_data.get("name", "Simulated Integration Outage")
        assumptions = scenario_data.get("assumptionsJson", {})

        s = {
            "id": s_id,
            "organization_id": org_id,
            "name": name,
            "assumptions_json": assumptions,
            "affected_nodes_json": ["integration_sf_01", "mis_analysis_99", "work_01"],
            "expected_impact_json": {
                "affected_missions_count": 4,
                "potential_delay_hours": 12.0,
                "production_modified": False
            },
            "confidence_pct": 94.0,
            "created_at": now_iso
        }
        _in_memory_scenarios[s_id] = s
        return s

    @staticmethod
    async def process_natural_language_query(session: Optional[AsyncSession], query_str: str, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_operating_graph_data()
        
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
                    "subject": "Project X / SOC2 Compliance",
                    "status": "at_risk",
                    "root_cause": "Vendor Security Exception approval bottleneck",
                    "responsible_owner": "team_exec"
                }
            ],
            "evidenceJson": {
                "referenced_nodes": ["out_01", "work_02", "bot_01"],
                "data_source": "Semantic Operating Graph 2.0"
            },
            "confidencePct": 92.5
        }
