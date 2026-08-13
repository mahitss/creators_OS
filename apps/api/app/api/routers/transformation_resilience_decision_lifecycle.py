from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_decision_lifecycle import (
    TransformationResilienceDecisionDomainRead,
    TransformationResilienceDecisionQuestionRead,
    TransformationResilienceDecisionContextRead,
    TransformationResilienceDecisionEvidencePackRead,
    TransformationResilienceDecisionAssumptionRead,
    TransformationResilienceDecisionOptionRead,
    TransformationResilienceDecisionTradeoffRead,
    TransformationResilienceDecisionRecommendationRead,
    TransformationResilienceDecisionRead,
    TransformationResilienceDecisionQueryResultRead
)
from app.services.transformation_resilience_decision_lifecycle_service import TransformationResilienceDecisionLifecycleService

router = APIRouter(prefix="/api/v1/transformation-resilience-decisions", tags=["transformation_resilience_decisions"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_decision_lifecycle_overview():
    return await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)

@router.post("", response_model=dict)
async def create_decision_domain(data: dict):
    return {
        "id": "dec_res_new",
        "decision_title": data.get("title", "New Resilience Decision Question"),
        "status": "pending_decision"
    }

@router.get("/similar", response_model=List[dict])
async def list_similar_decisions():
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    return overview.get("precedents", [])

@router.post("/query", response_model=TransformationResilienceDecisionQueryResultRead)
async def process_decision_query(query: str = Query(...)):
    return await TransformationResilienceDecisionLifecycleService.process_natural_language_decision_query(None, query)

@router.get("/{id}", response_model=dict)
async def get_decision(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    for d in overview.get("decisions", []):
        if d.get("id") == id:
            return d
    return {"id": id, "decision_title": "Active-Active Multi-Region Identity Gateway Architecture Decision", "status": "pending_decision"}

@router.get("/{id}/question", response_model=dict)
async def get_decision_question(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    questions = overview.get("questions", [])
    return questions[0] if questions else {}

@router.get("/{id}/context", response_model=dict)
async def get_decision_context(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    contexts = overview.get("contexts", [])
    return contexts[0] if contexts else {}

@router.get("/{id}/evidence", response_model=dict)
async def get_decision_evidence(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    evpacks = overview.get("evidencePacks", [])
    return evpacks[0] if evpacks else {}

@router.post("/{id}/evidence", response_model=dict)
async def add_decision_evidence(id: str, data: dict):
    return {"status": "added", "evidence_item": data}

@router.get("/{id}/assumptions", response_model=List[dict])
async def list_decision_assumptions(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    return overview.get("assumptions", [])

@router.get("/{id}/options", response_model=List[dict])
async def list_decision_options(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    return overview.get("options", [])

@router.post("/{id}/options", response_model=dict)
async def add_decision_option(id: str, data: dict):
    return {"id": "opt_new", "title": data.get("title", "New Option")}

@router.get("/{id}/scenarios", response_model=dict)
async def get_decision_scenarios(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    scenarios = overview.get("scenarios", [])
    return scenarios[0] if scenarios else {}

@router.post("/{id}/simulate", response_model=dict)
async def simulate_decision_scenarios(id: str, data: dict):
    return {
        "status": "completed",
        "scenarios_evaluated": ["baseline", "stress", "severe", "multi-failure"],
        "recommended_option_score": 0.96
    }

@router.get("/{id}/tradeoffs", response_model=dict)
async def get_decision_tradeoffs(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    tradeoffs = overview.get("tradeoffs", [])
    return tradeoffs[0] if tradeoffs else {}

@router.get("/{id}/recommendation", response_model=dict)
async def get_decision_recommendation(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    recs = overview.get("recommendations", [])
    return recs[0] if recs else {}

@router.post("/{id}/recommendation", response_model=dict)
async def update_decision_recommendation(id: str, data: dict):
    return {"status": "updated", "label": "RECOMMENDATION - NOT DECISION"}

@router.get("/{id}/approvals", response_model=List[dict])
async def list_decision_approvals(id: str):
    return [
        {"approver": "PolicyEngine", "status": "approved", "timestamp": "2026-08-13T10:00:00Z"},
        {"approver": "Enterprise Executive Board", "status": "pending_review", "conditions": ["Budget validation"]}
    ]

@router.post("/{id}/submit-approval", response_model=dict)
async def submit_decision_approval(id: str, data: dict):
    return {"status": "submitted_to_approval_engine", "approval_id": "appr_99"}

@router.post("/{id}/decide", response_model=dict)
async def decide_resilience_question(id: str, data: dict):
    selected_opt = data.get("selected_option_id", "opt_01")
    rationale = data.get("rationale", "Human owner approval")
    decider = data.get("decider_id", "Chief Resilience Officer")
    return await TransformationResilienceDecisionLifecycleService.make_decision(None, id, selected_opt, rationale, decider)

@router.get("/{id}/consequences", response_model=dict)
async def get_decision_consequences(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    consequences = overview.get("consequences", [])
    return consequences[0] if consequences else {}

@router.get("/{id}/timeline", response_model=List[dict])
async def get_decision_timeline(id: str):
    return [
        {"timestamp": "2026-08-13T09:00:00Z", "stage": "signal_detected", "summary": "OAuth Gateway P99 latency drift flagged."},
        {"timestamp": "2026-08-13T09:30:00Z", "stage": "question_framed", "summary": "Decision question dec_q_01 framed for pinv_01 funding."},
        {"timestamp": "2026-08-13T10:00:00Z", "stage": "scenarios_evaluated", "summary": "Evaluated Option A, B, and C across 5 stress scenarios."},
        {"timestamp": "2026-08-13T10:30:00Z", "stage": "recommendation_drafted", "summary": "Drafted recommendation for Option A (Tagged: RECOMMENDATION - NOT DECISION)."},
        {"timestamp": "2026-08-13T11:00:00Z", "stage": "approval_submitted", "summary": "Submitted packet to PolicyEngine and Enterprise Board."}
    ]

@router.get("/{id}/execution", response_model=dict)
async def get_decision_execution(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    exec_plans = overview.get("executionPlans", [])
    return exec_plans[0] if exec_plans else {}

@router.post("/{id}/execute", response_model=dict)
async def execute_decision_via_gateway(id: str, data: dict):
    return await TransformationResilienceDecisionLifecycleService.execute_decision(None, id, data)

@router.get("/{id}/verification", response_model=dict)
async def get_decision_verification(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    verifs = overview.get("verifications", [])
    return verifs[0] if verifs else {}

@router.post("/{id}/verify", response_model=dict)
async def verify_decision_outcomes(id: str, data: dict):
    return {"status": "verified", "variance_pct": 2.1, "confidence": 0.96}

@router.get("/{id}/effectiveness", response_model=dict)
async def get_decision_effectiveness(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    effs = overview.get("effectivenesses", [])
    return effs[0] if effs else {}

@router.get("/{id}/reviews", response_model=List[dict])
async def list_decision_reviews(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    return overview.get("reviews", [])

@router.post("/{id}/reviews", response_model=dict)
async def trigger_decision_review(id: str, data: dict):
    return {"status": "review_requested", "reason": data.get("reason", "Assumption drift")}

@router.post("/{id}/reopen", response_model=dict)
async def reopen_decision(id: str, data: dict):
    return {"status": "reopened", "historical_record_preserved": True}

@router.get("/{id}/precedents", response_model=List[dict])
async def list_decision_precedents(id: str):
    overview = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
    return overview.get("precedents", [])
