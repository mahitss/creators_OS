from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_assurance_intelligence import (
    TransformationResilienceAssuranceDecisionIntelligenceDomainRead,
    TransformationResilienceAssuranceDecisionOutcomeRead,
    TransformationResilienceAssuranceExpectedActualComparisonRead,
    TransformationResilienceAssuranceOutcomeVarianceRead,
    TransformationResilienceAssuranceOutcomeEvidenceRead,
    TransformationResilienceAssuranceOutcomeCausalAnalysisRead,
    TransformationResilienceAssuranceRecommendationQualityRead,
    TransformationResilienceAssuranceDecisionQualityRead,
    TransformationResilienceAssuranceDecisionQualityTrendRead,
    TransformationResilienceAssuranceResolutionPatternPerformanceRead,
    TransformationResilienceAssuranceContextSimilarityRead,
    TransformationResilienceAssuranceHistoricalAnalogueRead,
    TransformationResilienceAssuranceRecommendationCalibrationRead,
    TransformationResilienceAssuranceLearningSignalRead,
    TransformationResilienceAssuranceLearningPriorityRead,
    TransformationResilienceAssuranceKnowledgeUpdateProposalRead,
    TransformationResilienceAssuranceRecommendationUpdateProposalRead,
    TransformationResilienceAssuranceLearningVersionRead,
    TransformationResilienceAssuranceRecommendationRegressionRead,
    TransformationResilienceAssuranceRecommendationDriftRead,
    TransformationResilienceAssuranceLessonRead,
    TransformationResilienceAssuranceLessonQualityRead,
    TransformationResilienceAssuranceQueryResultRead
)
from app.services.transformation_resilience_assurance_intelligence_service import TransformationResilienceAssuranceIntelligenceService

router = APIRouter(prefix="/api/v1/transformation-resilience-assurance-intelligence", tags=["transformation_resilience_assurance_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_assurance_intelligence_overview():
    return await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)

@router.post("", response_model=dict)
async def create_assurance_intelligence_domain(data: dict):
    return {
        "id": "adom_new",
        "name": data.get("name", "New Assurance Decision Intelligence Domain"),
        "scope": data.get("scope", "enterprise"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceAssuranceQueryResultRead)
async def process_assurance_intelligence_query(query: str = Query(...)):
    return await TransformationResilienceAssuranceIntelligenceService.process_natural_language_assurance_intelligence_query(None, query)

@router.get("/outcomes", response_model=List[dict])
async def list_decision_outcomes():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("outcomes", [])

@router.get("/outcomes/{id}", response_model=dict)
async def get_decision_outcome(id: str):
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    for doc in overview.get("outcomes", []):
        if doc.get("id") == id:
            return doc
    return {"id": id, "selected_option": "sequence", "outcome_status": "positive"}

@router.get("/recommendation-quality", response_model=List[dict])
async def list_recommendation_quality():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("recommendationQualities", [])

@router.get("/decision-quality", response_model=List[dict])
async def list_decision_quality():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("decisionQualities", [])

@router.get("/pattern-performance", response_model=List[dict])
async def list_pattern_performance():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("patternPerformances", [])

@router.get("/historical-analogues", response_model=List[dict])
async def list_historical_analogues():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("historicalAnalogues", [])

@router.get("/calibration", response_model=List[dict])
async def list_calibrations():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("calibrations", [])

@router.get("/drift", response_model=List[dict])
async def list_drifts():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("drifts", [])

@router.get("/learning-signals", response_model=List[dict])
async def list_learning_signals():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("learningSignals", [])

@router.post("/learning-signals", response_model=dict)
async def create_learning_signal(data: dict):
    return {
        "id": "lsig_new",
        "signal_type": data.get("signal_type", "recurring_pattern"),
        "description": data.get("description", "New learning signal detected."),
        "priority": data.get("priority", "high")
    }

@router.get("/lessons", response_model=List[dict])
async def list_lessons():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("lessons", [])

@router.get("/update-proposals", response_model=List[dict])
async def list_update_proposals():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    props = []
    props.extend(overview.get("knowledgeUpdateProposals", []))
    props.extend(overview.get("recommendationUpdateProposals", []))
    return props

@router.post("/update-proposals", response_model=dict)
async def create_update_proposal(data: dict):
    return {
        "id": "prop_new",
        "proposal_type": data.get("proposal_type", "new_validation_requirement"),
        "description": data.get("description", "New knowledge update proposal."),
        "status": "pending_review"
    }

@router.post("/shadow-evaluation", response_model=dict)
async def run_shadow_evaluation(data: dict):
    return await TransformationResilienceAssuranceIntelligenceService.run_shadow_evaluation(None, data)

@router.get("/shadow-evaluation", response_model=List[dict])
async def list_shadow_evaluations():
    return [{
        "id": "seval_01",
        "production_recommendation": "sequence",
        "shadow_recommendation": "sequence_with_capacity_buffer",
        "status": "completed"
    }]

@router.get("/regressions", response_model=List[dict])
async def list_regressions():
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    return overview.get("regressions", [])

@router.post("/update-proposals/{id}/request-approval", response_model=dict)
async def request_proposal_approval(id: str):
    return await TransformationResilienceAssuranceIntelligenceService.request_proposal_approval(None, id)

@router.get("/update-proposals/{id}/approval", response_model=dict)
async def get_proposal_approval(id: str):
    return {"proposal_id": id, "approval_state": "approved", "approver": "Governance Board"}

@router.get("/{id}", response_model=dict)
async def get_assurance_intelligence_domain(id: str):
    overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
    for dom in overview.get("domains", []):
        if dom.get("id") == id:
            return dom
    return {"id": id, "name": "Global Enterprise Assurance Decision Intelligence Domain", "status": "active"}
