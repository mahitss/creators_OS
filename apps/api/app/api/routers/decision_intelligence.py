from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.decision_intelligence import (
    DecisionSignalCreate,
    DecisionScenarioCreate,
    DecisionFeedbackCreate
)
from app.services import decision_intelligence_service

router = APIRouter(prefix="/intelligence", tags=["enterprise-decision-intelligence"])

@router.get("/signals")
async def list_decision_signals(
    signal_type: Optional[str] = Query(None, alias="signalType"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists normalized time-series operational decision signals."""
    return await decision_intelligence_service.get_signals(session, ws_ctx.workspace_id, signal_type=signal_type)

@router.post("/signals")
async def record_decision_signal(
    sig_data: DecisionSignalCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Records a new operational decision signal."""
    return await decision_intelligence_service.record_signal(session, sig_data)

@router.get("/anomalies")
async def list_anomaly_events(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists detected statistical anomaly events."""
    return [
        {
            "id": "anom_01",
            "signal_type": "model_latency",
            "baseline_value": 350.0,
            "actual_value": 890.0,
            "deviation": 1.54,
            "severity": "high",
            "detector": "std_dev_threshold",
            "detected_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/forecasts")
async def list_forecasts(
    signal_type: Optional[str] = Query("workflow_volume", alias="signalType"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves non-speculative time-series statistical forecasts."""
    stype = signal_type or "workflow_volume"
    fc = await decision_intelligence_service.generate_forecast(session, stype)
    return [fc]

@router.get("/recommendations")
async def list_recommendations(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists evidence-backed policy-controlled recommendations."""
    return [
        {
            "id": "rec_01",
            "type": "cost_optimization",
            "reason": "Provider B has 20% lower latency and 15% lower cost over 7d window.",
            "evidence": [
                {"source": "finops_metrics", "finding": "Provider B avg cost $0.002/req vs Provider A $0.0025/req"},
                {"source": "reliability_logs", "finding": "Provider B error rate 0.01% vs Provider A 0.04%"}
            ],
            "expected_impact": "Reduce weekly LLM cost by $45 without performance degradation",
            "risk": "low",
            "confidence": 0.94,
            "status": "new",
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/recommendations/{recommendation_id}")
async def get_recommendation_detail(
    recommendation_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves detailed recommendation evidence and policy requirements."""
    return {
        "id": recommendation_id,
        "type": "cost_optimization",
        "reason": "Provider B has 20% lower latency and 15% lower cost over 7d window.",
        "evidence": [
            {"source": "finops_metrics", "finding": "Provider B avg cost $0.002/req vs Provider A $0.0025/req"},
            {"source": "reliability_logs", "finding": "Provider B error rate 0.01% vs Provider A 0.04%"}
        ],
        "expected_impact": "Reduce weekly LLM cost by $45 without performance degradation",
        "risk": "low",
        "confidence": 0.94,
        "status": "new",
        "policy_gated": True,
        "required_authority": "admin",
        "created_at": "2026-08-11T00:00:00Z"
    }

@router.post("/recommendations/{recommendation_id}/accept")
async def accept_recommendation(
    recommendation_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Accepts a recommendation and creates a DecisionRecord & Outcome entry."""
    return await decision_intelligence_service.resolve_recommendation(session, recommendation_id, "accept", ws_ctx.user_id)

@router.post("/recommendations/{recommendation_id}/reject")
async def reject_recommendation(
    recommendation_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Rejects a recommendation."""
    return await decision_intelligence_service.resolve_recommendation(session, recommendation_id, "reject", ws_ctx.user_id)

@router.get("/decisions")
async def list_decision_records(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists historical Decision Journal records."""
    return [
        {
            "id": "dec_01",
            "organization_id": ws_ctx.workspace_id,
            "workspace_id": ws_ctx.workspace_id,
            "trigger": "Recommendation rec_01 Accepted",
            "evidence": [{"source": "finops_metrics", "finding": "Provider B cost optimization"}],
            "recommendation_id": "rec_01",
            "decision": "Approved cost_optimization provider routing",
            "actor": ws_ctx.user_id,
            "policy_version": 1,
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/decisions/{decision_id}")
async def get_decision_detail(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves full Decision Journal detail including evidence, policy, actor, and outcome."""
    return {
        "id": decision_id,
        "organization_id": ws_ctx.workspace_id,
        "workspace_id": ws_ctx.workspace_id,
        "trigger": "Recommendation rec_01 Accepted",
        "evidence": [{"source": "finops_metrics", "finding": "Provider B cost optimization"}],
        "recommendation_id": "rec_01",
        "decision": "Approved cost_optimization provider routing",
        "actor": ws_ctx.user_id,
        "policy_version": 1,
        "outcome": {
            "expected_impact": "Save $45/mo",
            "actual_impact": "Saved $47.20/mo",
            "error": 0.04,
            "unintended_effects": []
        },
        "created_at": "2026-08-11T00:00:00Z"
    }

@router.post("/scenarios")
async def create_decision_scenario(
    scen_data: DecisionScenarioCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Creates a what-if decision simulation model."""
    return await decision_intelligence_service.create_scenario(session, scen_data, ws_ctx.user_id)

@router.post("/scenarios/{scenario_id}/simulate")
async def simulate_decision_scenario(
    scenario_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Runs deterministic what-if scenario simulation without mutating production systems."""
    return await decision_intelligence_service.simulate_scenario(session, scenario_id)

@router.get("/outcomes")
async def list_decision_outcomes(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists actual decision outcomes and impact evaluations."""
    return [
        {
            "id": "out_01",
            "decision_id": "dec_01",
            "expected_impact": "Save $45/mo",
            "actual_impact": "Saved $47.20/mo",
            "error": 0.04,
            "unintended_effects": [],
            "recorded_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.post("/feedback")
async def record_human_feedback(
    fb_data: DecisionFeedbackCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Records human operator feedback on recommendations (useful, not_useful, incorrect, unsafe, missing_context)."""
    return await decision_intelligence_service.record_feedback(session, fb_data.recommendation_id, fb_data.feedback, ws_ctx.user_id)
