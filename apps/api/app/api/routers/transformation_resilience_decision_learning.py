from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_decision_learning import (
    TransformationResilienceDecisionLearningDomainRead,
    TransformationResilienceDecisionExpectedOutcomeRead,
    TransformationResilienceDecisionObservedOutcomeRead,
    TransformationResilienceDecisionOutcomeComparisonRead,
    TransformationResilienceDecisionAttributionRead,
    TransformationResilienceDecisionExternalFactorRead,
    TransformationResilienceDecisionFailureAnalysisRead,
    TransformationResilienceDecisionSuccessPatternRead,
    TransformationResilienceDecisionFailurePatternRead,
    TransformationResilienceDecisionLessonRead,
    TransformationResilienceDecisionLessonConflictRead,
    TransformationResilienceDecisionQualityAssessmentRead,
    TransformationResilienceDecisionCalibrationRead,
    TransformationResilienceDecisionModelPerformanceRead,
    TransformationResilienceDecisionDelayAnalysisRead,
    TransformationResilienceDecisionLearningQueryResultRead
)
from app.services.transformation_resilience_decision_learning_service import TransformationResilienceDecisionLearningService

router = APIRouter(prefix="/api/v1/transformation-resilience-decision-learning", tags=["transformation_resilience_decision_learning"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_decision_learning_overview():
    return await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)

@router.post("", response_model=dict)
async def create_learning_domain(data: dict):
    return {
        "id": "learn_dom_new",
        "name": data.get("name", "New Decision Learning Domain"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceDecisionLearningQueryResultRead)
async def process_learning_query(query: str = Query(...)):
    return await TransformationResilienceDecisionLearningService.process_natural_language_learning_query(None, query)

@router.get("/{id}", response_model=dict)
async def get_learning_domain(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    for dom in overview.get("domains", []):
        if dom.get("id") == id:
            return dom
    return {"id": id, "name": "Global Enterprise Continuous Resilience Decision Quality & Outcome Intelligence 2.0", "status": "active"}

@router.get("/{id}/expected-outcomes", response_model=List[dict])
async def list_expected_outcomes(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("expectedOutcomes", [])

@router.get("/{id}/observed-outcomes", response_model=List[dict])
async def list_observed_outcomes(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("observedOutcomes", [])

@router.get("/{id}/comparisons", response_model=List[dict])
async def list_outcome_comparisons(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("comparisons", [])

@router.get("/{id}/effectiveness", response_model=dict)
async def get_effectiveness_summary(id: str):
    return {
        "resilienceImprovement": 0.05,
        "riskReductionPct": 65.0,
        "recoveryImprovement": "+15.0%",
        "benefitPreservation": 0.98,
        "unintendedConsequences": None
    }

@router.get("/{id}/attribution", response_model=List[dict])
async def list_attributions(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("attributions", [])

@router.get("/{id}/external-factors", response_model=List[dict])
async def list_external_factors(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("externalFactors", [])

@router.get("/{id}/success-patterns", response_model=List[dict])
async def list_success_patterns(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("successPatterns", [])

@router.get("/{id}/failure-patterns", response_model=List[dict])
async def list_failure_patterns(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("failurePatterns", [])

@router.get("/{id}/patterns", response_model=List[dict])
async def list_decision_patterns(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("decisionPatterns", [])

@router.get("/{id}/precedents", response_model=List[dict])
async def list_precedents(id: str):
    return [
        {
            "id": "prec_01",
            "prior_decision_id": "dec_hist_2025_04",
            "context": "2025 SSO Cluster Multi-Region Expansion",
            "applicability": 0.92,
            "historical_outcome_preserved": True
        }
    ]

@router.get("/{id}/lessons", response_model=List[dict])
async def list_lessons(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("lessons", [])

@router.post("/{id}/lessons", response_model=dict)
async def create_lesson(id: str, data: dict):
    return await TransformationResilienceDecisionLearningService.create_lesson(None, data)

@router.get("/{id}/lesson-conflicts", response_model=List[dict])
async def list_lesson_conflicts(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("lessonConflicts", [])

@router.get("/{id}/lesson-applications", response_model=List[dict])
async def list_lesson_applications(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("lessonApplications", [])

@router.get("/{id}/quality", response_model=List[dict])
async def list_quality_assessments(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("qualityAssessments", [])

@router.get("/{id}/calibration", response_model=List[dict])
async def list_calibrations(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("calibrations", [])

@router.get("/{id}/scenario-learning", response_model=dict)
async def get_scenario_learning(id: str):
    return {
        "evaluated_scenarios_count": 5,
        "scenario_blind_spots": ["Secondary vendor maintenance window overlap"],
        "accuracy_pct": 96.0
    }

@router.get("/{id}/simulation-learning", response_model=List[dict])
async def list_simulation_learning(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("modelPerformances", [])

@router.get("/{id}/delay-analysis", response_model=List[dict])
async def list_delay_analysis(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("delayAnalyses", [])

@router.get("/{id}/counterfactuals", response_model=List[dict])
async def list_counterfactuals(id: str):
    overview = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
    return overview.get("counterfactuals", [])
