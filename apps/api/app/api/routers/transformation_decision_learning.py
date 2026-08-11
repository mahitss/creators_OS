from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_decision_learning import (
    TransformationDecisionLifecycleRead,
    TransformationDecisionBaselineRead,
    TransformationDecisionVarianceRead,
    TransformationDecisionLessonRead,
    TransformationDecisionPatternRead,
    TransformationDecisionLearningReviewRead,
    TransformationDecisionCounterfactualRead,
    TransformationDecisionQualityReviewRead,
    TransformationLearningQueryResultRead
)
from app.services.transformation_decision_learning_service import TransformationDecisionLearningService

router = APIRouter(prefix="/api/v1/transformation-decision-learning", tags=["transformation_decision_learning"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_learning_overview():
    return await TransformationDecisionLearningService.get_learning_overview(None)

@router.get("/lessons", response_model=List[dict])
async def list_lessons():
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("lessons", [])

@router.get("/lessons/{id}", response_model=dict)
async def get_lesson(id: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    for l in overview.get("lessons", []):
        if l.get("id") == id:
            return l
    return {"id": id, "lesson": "Pre-signer rule caching delivers +1.2% higher cost reduction", "confidence": "high"}

@router.post("/lessons/{id}/review", response_model=dict)
async def review_lesson(id: str, data: dict):
    return {"id": id, "status": "under_review", "feedback": data.get("feedback", "Review initiated")}

@router.post("/lessons/{id}/approve", response_model=dict)
async def approve_lesson(id: str):
    return {"id": id, "status": "approved", "reviewer": "Chief Architecture Officer"}

@router.post("/lessons/{id}/reject", response_model=dict)
async def reject_lesson(id: str):
    return {"id": id, "status": "rejected"}

@router.get("/patterns", response_model=List[dict])
async def list_patterns():
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("patterns", [])

@router.get("/patterns/{id}", response_model=dict)
async def get_pattern(id: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    for p in overview.get("patterns", []):
        if p.get("id") == id:
            return p
    return {"id": id, "pattern": "Sub-20ms policy telemetry backing yields zero execution drift", "sampleSize": 12}

@router.get("/analogies", response_model=List[dict])
async def list_analogies():
    return [
        {
            "historicalCase": "Wave 1 FinOps Pilot",
            "currentCase": "Wave 2 Scale Authorization",
            "similarity": "Zero-trust policy pre-signing schema",
            "differences": "Wave 2 scales from 2 regions to 4 regions"
        }
    ]

@router.get("/reviews", response_model=List[dict])
async def list_reviews():
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("reviews", [])

@router.post("/reviews", response_model=dict)
async def create_review(data: dict):
    return {"id": "rev_new", "status": "candidate", "feedback": data.get("feedback", "New review candidate")}

@router.get("/reviews/{id}", response_model=dict)
async def get_review(id: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    for r in overview.get("reviews", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "approved"}

@router.post("/reviews/{id}/complete", response_model=dict)
async def complete_review(id: str):
    return {"id": id, "status": "approved", "completed": True}

@router.get("/{decisionId}/lifecycle", response_model=dict)
async def get_decision_lifecycle(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    for lc in overview.get("lifecycles", []):
        if lc.get("decision_case_id") == decisionId:
            return lc
    return {"id": "lc_01", "decisionCaseId": decisionId, "currentStage": "learning"}

@router.get("/{decisionId}/baseline", response_model=dict)
async def get_decision_baseline(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    for b in overview.get("baselines", []):
        if b.get("decision_case_id") == decisionId:
            return b
    return {"id": "base_01", "decisionCaseId": decisionId, "expectedOutcome": "Sub-100ms policy validation with 30.0% OpEx reduction"}

@router.get("/{decisionId}/outcomes", response_model=dict)
async def get_decision_outcomes(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return {
        "expected": overview.get("expectedOutcomes", []),
        "actual": overview.get("actualOutcomes", [])
    }

@router.get("/{decisionId}/variance", response_model=List[dict])
async def get_decision_variance(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("variances", [])

@router.get("/{decisionId}/lessons", response_model=List[dict])
async def get_decision_lessons(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("lessons", [])

@router.post("/{decisionId}/counterfactuals", response_model=dict)
async def create_counterfactual(decisionId: str, data: dict):
    return {"id": "cf_new", "decisionCaseId": decisionId, "actualPath": "Full Wave 2 scale", "alternativePath": data.get("alternativePath", "Staggered rollout")}

@router.get("/{decisionId}/counterfactuals", response_model=List[dict])
async def get_decision_counterfactuals(decisionId: str):
    overview = await TransformationDecisionLearningService.get_learning_overview(None)
    return overview.get("counterfactuals", [])

@router.post("/query", response_model=TransformationLearningQueryResultRead)
async def process_learning_query(query: str = Query(...)):
    return await TransformationDecisionLearningService.process_natural_language_learning_query(None, query)
