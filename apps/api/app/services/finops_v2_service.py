import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import model_gateway_service, governance_service

_in_memory_usage_events: List[dict] = []
_in_memory_price_catalog: Dict[str, dict] = {}
_in_memory_cost_calculations: List[dict] = []
_in_memory_budgets: Dict[str, dict] = {}
_in_memory_forecasts: Dict[str, dict] = {}
_in_memory_drivers: List[dict] = []
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_finops_experiments: Dict[str, dict] = {}
_in_memory_anomalies: List[dict] = []
_in_memory_adjustments: List[dict] = []
_in_memory_reconciliations: List[dict] = []

def _initialize_seed_finops_v2_data():
    if _in_memory_price_catalog:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Price Catalog
    p1 = {
        "id": "price_gpt4o_v1",
        "provider": "openai",
        "model": "gpt-4o",
        "unit": "1k_tokens",
        "price": 0.005,
        "currency": "USD",
        "effective_from": now_iso,
        "effective_to": None,
        "source": "openai_pricing_v1",
        "version": 1,
        "updated_at": now_iso
    }
    p2 = {
        "id": "price_gemini_v1",
        "provider": "google",
        "model": "gemini-1.5-pro",
        "unit": "1k_tokens",
        "price": 0.0035,
        "currency": "USD",
        "effective_from": now_iso,
        "effective_to": None,
        "source": "google_vertex_v1",
        "version": 1,
        "updated_at": now_iso
    }
    _in_memory_price_catalog[p1["model"]] = p1
    _in_memory_price_catalog[p2["model"]] = p2

    # Seed Budgets
    b1 = {
        "id": "bgt_org_01",
        "organization_id": org_id,
        "workspace_id": None,
        "team_id": None,
        "agent_id": None,
        "mission_id": None,
        "scope": "organization",
        "period": "monthly",
        "limit_amount": 2500.0,
        "currency": "USD",
        "spent_amount": 420.0,
        "committed_amount": 150.0,
        "forecast_amount": 1850.0,
        "remaining_amount": 1930.0,
        "soft_threshold_pct": 75.0,
        "hard_limit_action": "require_approval",
        "status": "healthy"
    }
    _in_memory_budgets[b1["id"]] = b1

    # Seed Recommendations
    r1 = {
        "id": "rec_model_switch_01",
        "organization_id": org_id,
        "type": "model_switch",
        "estimated_savings": 145.0,
        "quality_impact": "neutral",
        "latency_impact": "improved",
        "risk_level": "low",
        "confidence_pct": 94.5,
        "evidence_json": {
            "proposed_model": "gemini-1.5-pro",
            "current_model": "gpt-4o",
            "eval_quality_score": 4.85,
            "quality_threshold": 4.5
        },
        "approval_status": "pending",
        "created_at": now_iso
    }
    _in_memory_recommendations[r1["id"]] = r1

    # Seed Forecast
    _in_memory_forecasts[org_id] = {
        "id": "fc_org_01",
        "organization_id": org_id,
        "scope": "organization",
        "current_period_expected": 1850.0,
        "lower_bound": 1600.0,
        "upper_bound": 2100.0,
        "confidence_pct": 91.0,
        "created_at": now_iso
    }

_initialize_seed_finops_v2_data()


class FinOpsV2Service:

    @staticmethod
    async def record_usage_event(session: Optional[AsyncSession], usage_data: dict) -> dict:
        _initialize_seed_finops_v2_data()
        evt_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        evt = {
            "id": evt_id,
            "organization_id": usage_data.get("organizationId", "org_default_creator"),
            "workspace_id": usage_data.get("workspaceId", "ws_default"),
            "agent_id": usage_data.get("agentId"),
            "mission_id": usage_data.get("missionId"),
            "decision_id": usage_data.get("decisionId"),
            "workflow_id": usage_data.get("workflowId"),
            "model_id": usage_data.get("modelId", "gemini-1.5-pro"),
            "provider_id": usage_data.get("providerId", "google"),
            "capability_id": usage_data.get("capabilityId"),
            "usage_type": usage_data.get("usageType", "model_input"),
            "units_used": usage_data.get("unitsUsed", 1.0),
            "tokens_input": usage_data.get("tokensInput", 0),
            "tokens_output": usage_data.get("tokensOutput", 0),
            "tokens_cached": usage_data.get("tokensCached", 0),
            "tokens_reasoning": usage_data.get("tokensReasoning", 0),
            "latency_ms": usage_data.get("latencyMs", 120.0),
            "timestamp": now_iso
        }
        _in_memory_usage_events.append(evt)

        # Calculate Cost
        price_rec = _in_memory_price_catalog.get(evt["model_id"])
        price_val = price_rec["price"] if price_rec else 0.003
        price_ver_id = price_rec["id"] if price_rec else "price_default"
        cost_status = "estimated" if price_rec else "unknown"

        calc_cost = ((evt["tokens_input"] + evt["tokens_output"]) / 1000.0) * price_val
        cost_calc = {
            "id": str(uuid.uuid4()),
            "usage_event_id": evt_id,
            "price_version_id": price_ver_id,
            "units": evt["units_used"],
            "estimated_cost": calc_cost,
            "actual_cost": None,
            "currency": "USD",
            "cost_status": cost_status,
            "organization_id": evt["organization_id"],
            "workspace_id": evt["workspace_id"],
            "agent_id": evt["agent_id"],
            "mission_id": evt["mission_id"],
            "timestamp": now_iso
        }
        _in_memory_cost_calculations.append(cost_calc)

        return evt

    @staticmethod
    async def get_overview_dashboard(session: Optional[AsyncSession], organization_id: str = "org_default_creator") -> dict:
        _initialize_seed_finops_v2_data()
        total_estimated = sum(c["estimated_cost"] for c in _in_memory_cost_calculations if c["organization_id"] == organization_id)
        active_budgets = list(_in_memory_budgets.values())
        recs = list(_in_memory_recommendations.values())
        forecast = _in_memory_forecasts.get(organization_id)

        return {
            "totalSpend": total_estimated + 420.0, # Seed + live events
            "currency": "USD",
            "activeBudgetsCount": len(active_budgets),
            "recommendationsCount": len(recs),
            "estimatedMonthlySavings": sum(r["estimated_savings"] for r in recs if r["approval_status"] in ["pending", "approved"]),
            "anomaliesCount": len(_in_memory_anomalies),
            "forecast": forecast,
            "budgets": active_budgets,
            "recommendations": recs,
            "capacity": {
                "concurrencyUsed": 12,
                "concurrencyLimit": 50,
                "queueDepth": 4,
                "loadSheddingRecommended": False
            }
        }

    @staticmethod
    async def get_attributed_costs(session: Optional[AsyncSession], group_by: str = "model") -> List[dict]:
        _initialize_seed_finops_v2_data()
        if group_by == "model":
            return [
                {"model": "gpt-4o", "provider": "openai", "cost": 280.50, "requests": 1450, "tokens": 4200000},
                {"model": "gemini-1.5-pro", "provider": "google", "cost": 139.50, "requests": 2100, "tokens": 6800000}
            ]
        elif group_by == "agent":
            return [
                {"agent_id": "agent_analyst_01", "name": "Document Analyst Agent", "cost": 210.0, "missions": 45},
                {"agent_id": "agent_code_reviewer_02", "name": "Code Reviewer Agent", "cost": 210.0, "missions": 38}
            ]
        elif group_by == "mission":
            return [
                {"mission_id": "mis_analysis_99", "name": "Q3 Financial Data Analysis", "cost": 65.0, "status": "completed"},
                {"mission_id": "mis_audit_102", "name": "Security Audit Report Synthesis", "cost": 85.0, "status": "running"}
            ]
        return [
            {"workspace_id": "ws_default", "name": "Default Executive Workspace", "cost": 420.0}
        ]

    @staticmethod
    async def approve_recommendation(session: Optional[AsyncSession], rec_id: str) -> Optional[dict]:
        _initialize_seed_finops_v2_data()
        rec = _in_memory_recommendations.get(rec_id)
        if not rec:
            return None
        rec["approval_status"] = "approved"
        return rec

    @staticmethod
    async def apply_recommendation(session: Optional[AsyncSession], rec_id: str) -> Optional[dict]:
        _initialize_seed_finops_v2_data()
        rec = _in_memory_recommendations.get(rec_id)
        if not rec:
            return None
        rec["approval_status"] = "applied"
        return rec

    @staticmethod
    async def revert_recommendation(session: Optional[AsyncSession], rec_id: str) -> Optional[dict]:
        _initialize_seed_finops_v2_data()
        rec = _in_memory_recommendations.get(rec_id)
        if not rec:
            return None
        rec["approval_status"] = "reverted"
        return rec

    @staticmethod
    async def create_cost_adjustment(session: Optional[AsyncSession], adj_data: dict, user_id: str = "usr_sec_admin_01") -> dict:
        _initialize_seed_finops_v2_data()
        adj_id = str(uuid.uuid4())
        rec = {
            "id": adj_id,
            "cost_calculation_id": adj_data.get("costCalculationId", "calc_demo_01"),
            "original_amount": adj_data.get("originalAmount", 10.0),
            "adjusted_amount": adj_data.get("adjustedAmount", 8.0),
            "reason": adj_data.get("reason", "Audited pricing variance correction"),
            "adjusted_by_user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_adjustments.append(rec)
        await governance_service.record_audit_event(
            session, "org_default_creator", user_id, "cost_adjustment_recorded", "cost_calculation", rec["cost_calculation_id"]
        )
        return rec
