import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service, finops_v2_service

_in_memory_portfolios: Dict[str, dict] = {}
_in_memory_programs: Dict[str, dict] = {}
_in_memory_conflicts: Dict[str, dict] = {}
_in_memory_overlaps: Dict[str, dict] = {}
_in_memory_variances: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}

def _initialize_seed_portfolio_data():
    if _in_memory_portfolios:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Portfolio
    pf1 = {
        "id": "port_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Enterprise Strategic Investment Portfolio 2026",
        "description": "Portfolio covering core security, AI agent expansion, and cloud infrastructure initiatives.",
        "owner": "usr_exec_01",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_portfolios[pf1["id"]] = pf1

    # Seed Program
    prog1 = {
        "id": "prog_01",
        "portfolio_id": pf1["id"],
        "name": "Autonomous Agent Resilience & Security Program",
        "description": "Comprehensive security, threat fabric, and resilience engineering for AI agents.",
        "owner": "team_security",
        "status": "active",
        "priority": "critical",
        "target_outcome": "SOC2 & ISO 27001 Certified Security Fabric"
    }
    _in_memory_programs[prog1["id"]] = prog1

    # Seed Resource Conflict
    conf1 = {
        "id": "conf_01",
        "portfolio_id": pf1["id"],
        "resource_type": "agent_capacity",
        "competing_initiatives_json": ["init_01", "init_03"],
        "time_window": "Q3 2026",
        "capacity_gap_summary": "Both initiatives require 8 shared senior security agent worker nodes.",
        "status": "active"
    }
    _in_memory_conflicts[conf1["id"]] = conf1

    # Seed Overlap Signal
    ov1 = {
        "id": "ov_01",
        "portfolio_id": pf1["id"],
        "initiative_ids_json": ["init_02", "init_05"],
        "overlap_type": "capability",
        "similarity_summary": "Both initiatives build redundant vector search caching mechanisms.",
        "status": "active"
    }
    _in_memory_overlaps[ov1["id"]] = ov1

    # Seed Outcome Variance
    v1 = {
        "id": "var_01",
        "portfolio_id": pf1["id"],
        "initiative_id": "init_01",
        "variance_type": "behind",
        "expected_outcome": "Deploy Threat Intelligence Fabric by August 15",
        "measured_outcome": "Module 3 testing incomplete (September 01 estimated)",
        "delta_summary": "16-day schedule delay due to upstream API dependency."
    }
    _in_memory_variances[v1["id"]] = v1

    # Seed Recommendation with Gated Approval & Reversibility
    rec1 = {
        "id": "rec_01",
        "portfolio_id": pf1["id"],
        "recommendation": "Resequence Initiative 03 start date to resolve agent capacity conflict with Initiative 01.",
        "evidence_json": {"conflicting_resource": "agent_capacity", "delay_mitigation": "Prevents 3-week outage risk"},
        "alternatives_json": [
            {
                "option": "Option A: Resequence Start Date",
                "description": "Delay Initiative 03 kickoff by 2 weeks.",
                "reversibility": "reversible",
                "cost_impact": "$0"
            },
            {
                "option": "Option B: Expand GPU Compute Capacity",
                "description": "Provision 4 additional GPU compute nodes.",
                "reversibility": "partially_reversible",
                "cost_impact": "+$15,000/mo"
            }
        ],
        "tradeoffs_json": {
            "speed": "Medium",
            "cost": "Low ($0)",
            "risk": "Minimal",
            "reversibility": "reversible"
        },
        "reversibility": "reversible",
        "approval_status": "pending",
        "confidence_pct": 94.5
    }
    _in_memory_recommendations[rec1["id"]] = rec1

_initialize_seed_portfolio_data()


class PortfolioIntelligenceService:

    @staticmethod
    async def get_portfolio_overview(session: Optional[AsyncSession], portfolio_id: str = "port_01") -> dict:
        _initialize_seed_portfolio_data()
        portfolio = _in_memory_portfolios.get(portfolio_id, list(_in_memory_portfolios.values())[0])
        programs = list(_in_memory_programs.values())
        conflicts = list(_in_memory_conflicts.values())
        overlaps = list(_in_memory_overlaps.values())
        variances = list(_in_memory_variances.values())
        recommendations = list(_in_memory_recommendations.values())

        return {
            "portfolio": portfolio,
            "programsCount": len(programs),
            "resourceConflictsCount": len(conflicts),
            "overlapsCount": len(overlaps),
            "variancesCount": len(variances),
            "recommendationsCount": len(recommendations),
            "programs": programs,
            "conflicts": conflicts,
            "overlaps": overlaps,
            "variances": variances,
            "recommendations": recommendations,
            "portfolioHealthScore": 0.92
        }

    @staticmethod
    async def create_portfolio(session: Optional[AsyncSession], portfolio_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_portfolio_data()
        p_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        p = {
            "id": p_id,
            "organization_id": org_id,
            "workspace_id": portfolio_data.get("workspaceId", "ws_default"),
            "name": portfolio_data["name"],
            "description": portfolio_data["description"],
            "owner": portfolio_data["owner"],
            "status": "draft",
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_portfolios[p_id] = p
        return p

    @staticmethod
    async def process_natural_language_portfolio_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_portfolio_data()

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
                    "subject": "Initiative 01 vs Initiative 03",
                    "resource_type": "agent_capacity",
                    "conflict_status": "active",
                    "competing_units": 8,
                    "recommendation": "Resequence Initiative 03 kickoff by 2 weeks (Option A)"
                }
            ],
            "evidenceJson": {
                "referenced_conflicts": ["conf_01"],
                "referenced_recommendations": ["rec_01"],
                "data_source": "Portfolio Intelligence 2.0"
            },
            "confidencePct": 94.5
        }
