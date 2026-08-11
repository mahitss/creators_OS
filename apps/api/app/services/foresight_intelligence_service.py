import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_programs: Dict[str, dict] = {}
_in_memory_drivers: Dict[str, dict] = {}
_in_memory_trends: Dict[str, dict] = {}
_in_memory_shifts: Dict[str, dict] = {}
_in_memory_uncertainties: Dict[str, dict] = {}
_in_memory_assumptions: Dict[str, dict] = {}
_in_memory_scenarios: Dict[str, dict] = {}
_in_memory_indicators: Dict[str, dict] = {}
_in_memory_options: Dict[str, dict] = {}
_in_memory_bets: Dict[str, dict] = {}
_in_memory_exposures: Dict[str, dict] = {}
_in_memory_blind_spots: Dict[str, dict] = {}
_in_memory_triggers: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_red_teams: Dict[str, dict] = {}
_in_memory_memories: Dict[str, dict] = {}

def _initialize_seed_foresight_data():
    if _in_memory_programs:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Program
    prog1 = {
        "id": "fprog_5yr_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Global 2026-2031 Enterprise AI & Compute Transformation Foresight",
        "description": "5-Year strategic foresight program assessing autonomous multi-agent mesh, regional compute sovereignty, and AI cost dynamics.",
        "horizon": "5_year",
        "scope": "global_enterprise",
        "owner": "usr_chief_strategy_officer",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_programs[prog1["id"]] = prog1

    # Seed Future Driver
    driv1 = {
        "id": "fdriv_01",
        "program_id": prog1["id"],
        "type": "technology",
        "driver_name": "Autonomous Agent Mesh & Real-Time Cognitive Workflow Orchestration",
        "strength": "accelerating",
        "evidence_json": {"source": "Patent analytics & enterprise AI adoption benchmarks", "quality": "verified"}
    }
    _in_memory_drivers[driv1["id"]] = driv1

    # Seed Strategic Trend
    trnd1 = {
        "id": "strnd_01",
        "program_id": prog1["id"],
        "trend_name": "Shift from Static SaaS Subscriptions to Value-Based Autonomous Work Output Pricing",
        "direction": "increasing",
        "velocity": "high",
        "persistence": "high",
        "confidence": "high",
        "evidence_json": {"market_data": "35% annual increase in outcome-based enterprise contracts"}
    }
    _in_memory_trends[trnd1["id"]] = trnd1

    # Seed Strategic Assumption (Fragile status)
    assm1 = {
        "id": "sassm_01",
        "program_id": prog1["id"],
        "statement": "Primary US-East Cloud Provider inference unit costs will decay by 25% annually through 2029.",
        "source": "Historical GPU Moore's Law extrapolation",
        "confidence": "medium",
        "valid_until": now_iso,
        "status": "fragile"
    }
    _in_memory_assumptions[assm1["id"]] = assm1

    # Seed Future Scenario (Plausibility vs Probability Gated)
    scen1 = {
        "id": "fscen_01",
        "program_id": prog1["id"],
        "name": "Scenario A: Multi-Region Autonomous Agent Mesh Ubiquity (Disruption Future)",
        "description": "Enterprise workflows transition 80% of routine execution to autonomous agent DAGs under centralized zero-trust policy control.",
        "horizon": "5_year",
        "scenario_type": "disruption",
        "plausibility": "high",
        "assumptions_json": ["sassm_01"],
        "drivers_json": ["fdriv_01"],
        "uncertainties_json": ["Uncertainty: Global GPU wafer supply constraint severity"],
        "status": "active"
    }
    _in_memory_scenarios[scen1["id"]] = scen1

    # Seed Scenario Indicator & Trigger
    ind1 = {
        "id": "sind_01",
        "scenario_id": scen1["id"],
        "indicator_name": "Autonomous Agent API Execution Share (% of total Enterprise Workflows)",
        "baseline_val": 15.0,
        "threshold_val": 45.0,
        "current_val": 52.4,
        "direction": "increasing",
        "confidence": "high"
    }
    _in_memory_indicators[ind1["id"]] = ind1

    trig1 = {
        "id": "strig_01",
        "indicator_id": ind1["id"],
        "condition_expression": "current_val > threshold_val (52.4% > 45.0%)",
        "recommended_action": "review",
        "status": "active"
    }
    _in_memory_triggers[trig1["id"]] = trig1

    # Seed Reversible Strategic Option & Robustness Score
    opt1 = {
        "id": "sopt_01",
        "scenario_id": scen1["id"],
        "option_name": "Option 1: Deploy Multi-Cloud Fallback Router for Agent Model Inference",
        "option_type": "experiment",
        "reversibility": "highly_reversible",
        "robustness_score": 0.94,
        "status": "active"
    }
    _in_memory_options[opt1["id"]] = opt1

    # Seed Strategic Bet & Exposure
    bet1 = {
        "id": "sbet_01",
        "program_id": prog1["id"],
        "thesis": "Invest $500k in building proprietary Enterprise Skill Fabric & Capability Registry.",
        "investment_amount": 500000.0,
        "expected_outcomes_json": ["10x reduction in manual workflow creation latency"],
        "scenarios_json": ["fscen_01"],
        "evidence": "Proven efficiency gains across 40 internal pilot workspaces.",
        "review_date": now_iso,
        "status": "active"
    }
    _in_memory_bets[bet1["id"]] = bet1

    exp1 = {
        "id": "sexp_01",
        "program_id": prog1["id"],
        "dependency_name": "Single-Vendor GPU Cloud Provider Infrastructure",
        "capability_id": "cap_core_01",
        "scenario_id": scen1["id"],
        "severity": "high",
        "exposure_type": "assumption_dependence"
    }
    _in_memory_exposures[exp1["id"]] = exp1

    # Seed Red-Team Adversarial Scenario (Hypothetical label)
    red1 = {
        "id": "ared_01",
        "program_id": prog1["id"],
        "name": "Red-Team Stress Test: Global Transatlantic Fiber Cut & Single Cloud Blackout",
        "adversarial_thesis": "Hypothetical catastrophic disruption testing multi-region failover speed and offline memory caching.",
        "is_hypothetical": True,
        "status": "active"
    }
    _in_memory_red_teams[red1["id"]] = red1

_initialize_seed_foresight_data()


class ForesightIntelligenceService:

    @staticmethod
    async def get_foresight_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_foresight_data()
        programs = list(_in_memory_programs.values())
        drivers = list(_in_memory_drivers.values())
        trends = list(_in_memory_trends.values())
        assumptions = list(_in_memory_assumptions.values())
        scenarios = list(_in_memory_scenarios.values())
        indicators = list(_in_memory_indicators.values())
        options = list(_in_memory_options.values())
        bets = list(_in_memory_bets.values())
        exposures = list(_in_memory_exposures.values())
        red_teams = list(_in_memory_red_teams.values())

        fragile_count = sum(1 for a in assumptions if a["status"] in ["questioned", "fragile"])

        return {
            "programsCount": len(programs),
            "driversCount": len(drivers),
            "trendsCount": len(trends),
            "fragileAssumptionsCount": fragile_count,
            "scenariosCount": len(scenarios),
            "indicatorsCount": len(indicators),
            "optionsCount": len(options),
            "betsCount": len(bets),
            "exposuresCount": len(exposures),
            "redTeamScenariosCount": len(red_teams),
            "robustnessScore": 0.94,
            "programs": programs,
            "drivers": drivers,
            "trends": trends,
            "assumptions": assumptions,
            "scenarios": scenarios,
            "indicators": indicators,
            "options": options,
            "bets": bets,
            "exposures": exposures,
            "redTeams": red_teams
        }

    @staticmethod
    async def complete_foresight_review(session: Optional[AsyncSession], program_id: str, review_data: dict) -> dict:
        _initialize_seed_foresight_data()
        prog = _in_memory_programs.get(program_id)
        if not prog:
            return {"error": "Foresight program not found"}

        now_iso = datetime.now(timezone.utc).isoformat()
        rev_id = str(uuid.uuid4())
        review = {
            "id": rev_id,
            "program_id": program_id,
            "review_date": now_iso,
            "participants_json": review_data.get("participants", ["usr_chief_strategy_officer", "usr_threat_architect"]),
            "scenarios_reviewed_json": review_data.get("scenariosReviewed", ["fscen_01"]),
            "assumptions_challenged_json": review_data.get("assumptionsChallenged", ["sassm_01"]),
            "decisions_json": review_data.get("decisions", ["Approved Option 1 Multi-Cloud Router experiment"]),
            "actions_json": review_data.get("actions", ["Deploy active indicators for GPU unit costs"])
        }
        _in_memory_reviews[rev_id] = review

        return {
            "reviewId": rev_id,
            "programId": program_id,
            "completedAt": now_iso,
            "status": "completed",
            "message": "Strategic Foresight review completed and logged."
        }

    @staticmethod
    async def process_natural_language_foresight_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_foresight_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking employee career/future-value ranking)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["rank employee", "career prediction", "future value score", "individual career"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee future-value ranking, individual career prediction, or protected attribute inference."},
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
                    "program_name": "Global 2026-2031 Enterprise AI & Compute Transformation Foresight",
                    "horizon": "5_year",
                    "plausible_scenario": "Scenario A: Multi-Region Autonomous Agent Mesh Ubiquity",
                    "fragile_assumption": "sassm_01 (GPU inference unit cost 25% annual decay)",
                    "leading_indicator": "52.4% Agent API execution share (Threshold 45.0% breached)",
                    "robust_option": "Option 1: Deploy Multi-Cloud Fallback Router (Reversibility: highly_reversible, Robustness: 94%)",
                    "red_team_scenario": "Red-Team Stress Test: Global Transatlantic Fiber Cut (Hypothetical)"
                }
            ],
            "evidenceJson": {
                "referenced_program": "fprog_5yr_01",
                "data_source": "Enterprise Strategic Foresight & Long-Horizon Scenario Intelligence 2.0 Engine"
            },
            "confidencePct": 96.0
        }
