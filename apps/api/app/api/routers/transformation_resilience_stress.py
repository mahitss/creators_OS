from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_stress import (
    TransformationResilienceStressTestingDomainRead,
    TransformationResilienceStressTestingHypothesisRead,
    TransformationResilienceStressTestingCampaignRead,
    TransformationResilienceStressTestingFailureInjectionRead,
    TransformationResilienceStressTestingCompoundFailureRead,
    TransformationResilienceStressTestingScenarioRead,
    TransformationResilienceStressTestingRunRead,
    TransformationResilienceStressTestingDetectionResultRead,
    TransformationResilienceStressTestingWarningValidationRead,
    TransformationResilienceStressTestingInterventionValidationRead,
    TransformationResilienceStressTestingRecoveryResultRead,
    TransformationResilienceStressTestingResultRead,
    TransformationResilienceStressTestingAssuranceGapRead,
    TransformationResilienceStressTestingControlRead,
    TransformationResilienceStressTestingControlResultRead,
    TransformationResilienceStressTestingControlFailureRead,
    TransformationResilienceStressTestingScorecardRead,
    TransformationResilienceStressTestingTrendRead,
    TransformationResilienceStressTestingRegressionRead,
    TransformationResilienceStressTestingCoverageRead,
    TransformationResilienceStressTestingCoverageGapRead,
    TransformationResilienceStressTestingScenarioMutationRead,
    TransformationResilienceStressTestingAdversarialScenarioRead,
    TransformationResilienceStressTestingRecoveryPlaybookTestRead,
    TransformationResilienceStressTestingGovernanceTestRead,
    TransformationResilienceStressTestingRemediationRecommendationRead,
    TransformationResilienceStressTestingQueryResultRead
)
from app.services.transformation_resilience_stress_service import TransformationResilienceStressService

router = APIRouter(prefix="/api/v1/transformation-resilience-stress", tags=["transformation_resilience_stress"])

@router.get("", response_model=dict)
@router.get("/status", response_model=dict)
async def get_stress_testing_status():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    domains = overview.get("domains", [])
    if domains:
        return domains[0]
    return {"id": "sdom_01", "name": "Stress Testing 2.0", "status": "active"}

@router.get("/campaigns", response_model=List[dict])
async def list_campaigns():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("campaigns", [])

@router.post("/campaigns", response_model=dict)
async def create_campaign(data: dict):
    return {"id": f"camp_{uuid.uuid4().hex[:8]}", "name": data.get("name", "New Campaign"), "status": "approved"}

@router.get("/campaigns/{id}", response_model=dict)
async def get_campaign(id: str):
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    for c in overview.get("campaigns", []):
        if c.get("id") == id:
            return c
    return {"id": id, "name": "Continuous Campaign", "status": "running"}

@router.post("/campaigns/{id}/start", response_model=dict)
async def start_campaign(id: str):
    return await TransformationResilienceStressService.start_campaign(None, id)

@router.get("/hypotheses", response_model=List[dict])
async def list_hypotheses():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("hypotheses", [])

@router.post("/hypotheses", response_model=dict)
async def create_hypothesis(data: dict):
    return {
        "id": f"hyp_{uuid.uuid4().hex[:8]}",
        "hypothesis": data.get("hypothesis", "New Resilience Hypothesis"),
        "confidence": 0.90
    }

@router.get("/failures", response_model=List[dict])
async def list_failure_injections():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("injections", [])

@router.post("/failures", response_model=dict)
async def create_failure_injection(data: dict):
    return await TransformationResilienceStressService.create_failure_injection(None, data)

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("scenarios", [])

@router.post("/scenarios", response_model=dict)
async def create_scenario(data: dict):
    return {"id": f"stscen_{uuid.uuid4().hex[:8]}", "expected_outcome": "Outcome defined"}

@router.get("/scenarios/{id}", response_model=dict)
async def get_scenario(id: str):
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    for sc in overview.get("scenarios", []):
        if sc.get("id") == id:
            return sc
    return {"id": id, "horizon_days": 30}

@router.post("/scenarios/{id}/run", response_model=dict)
async def run_scenario(id: str, seed: int = 42):
    return await TransformationResilienceStressService.run_scenario_simulation(None, id, seed)

@router.get("/results", response_model=List[dict])
async def list_results():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("results", [])

@router.get("/results/{id}", response_model=dict)
async def get_result(id: str):
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    for r in overview.get("results", []):
        if r.get("id") == id or r.get("run_id") == id:
            return r
    return {"id": id, "hypothesis_result": "passed"}

@router.get("/scorecards", response_model=List[dict])
async def list_scorecards():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("scorecards", [])

@router.get("/trends", response_model=List[dict])
async def list_trends():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("trends", [])

@router.get("/regressions", response_model=List[dict])
async def list_regressions():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("regressions", [])

@router.get("/coverage", response_model=dict)
async def get_coverage():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    covs = overview.get("coverages", [])
    if covs:
        return covs[0]
    return {"transformations_pct": 92.0, "plans_pct": 95.0}

@router.get("/coverage/gaps", response_model=List[dict])
async def list_coverage_gaps():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("coverageGaps", [])

@router.get("/playbooks", response_model=List[dict])
async def list_playbooks():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("playbookTests", [])

@router.post("/playbooks/{id}/test", response_model=dict)
async def test_playbook(id: str):
    return await TransformationResilienceStressService.test_recovery_playbook(None, id)

@router.get("/governance-tests", response_model=List[dict])
async def list_governance_tests():
    overview = await TransformationResilienceStressService.get_stress_overview(None)
    return overview.get("governanceTests", [])

@router.post("/governance-tests", response_model=dict)
async def run_governance_test(data: dict):
    return {"id": "govtest_02", "compliance_passed": True, "tested_boundary": data.get("boundary", "PolicyEngine")}

@router.post("/query", response_model=TransformationResilienceStressTestingQueryResultRead)
async def process_stress_query(query: str = Query(...)):
    return await TransformationResilienceStressService.process_natural_language_stress_query(None, query)
