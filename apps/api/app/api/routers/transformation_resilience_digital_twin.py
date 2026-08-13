from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_digital_twin import (
    TransformationResilienceDigitalTwinDomainRead,
    TransformationResilienceDigitalTwinStateRead,
    TransformationResilienceDigitalTwinSnapshotRead,
    TransformationResilienceDigitalTwinSynchronizationRead,
    TransformationResilienceDigitalTwinStateDiffRead,
    TransformationResilienceDigitalTwinNodeRead,
    TransformationResilienceDigitalTwinRelationshipRead,
    TransformationResilienceDigitalTwinRealityComparisonRead,
    TransformationResilienceDigitalTwinScenarioForkRead,
    TransformationResilienceDigitalTwinScenarioStateRead,
    TransformationResilienceDigitalTwinCounterfactualChangeRead,
    TransformationResilienceDigitalTwinCounterfactualScenarioRead,
    TransformationResilienceDigitalTwinScenarioOutcomeRead,
    TransformationResilienceDigitalTwinCounterfactualComparisonRead,
    TransformationResilienceDigitalTwinStressScenarioRead,
    TransformationResilienceDigitalTwinExternalShockScenarioRead,
    TransformationResilienceDigitalTwinRecoveryScenarioRead,
    TransformationResilienceDigitalTwinExperimentRead,
    TransformationResilienceDigitalTwinExperimentResultRead,
    TransformationResilienceDigitalTwinValidationRead,
    TransformationResilienceDigitalTwinModelErrorRead,
    TransformationResilienceDigitalTwinDriftRead,
    TransformationResilienceDigitalTwinScenarioLibraryRead,
    TransformationResilienceDigitalTwinQueryResultRead
)
from app.services.transformation_resilience_digital_twin_service import TransformationResilienceDigitalTwinService

router = APIRouter(prefix="/api/v1/transformation-resilience-digital-twin", tags=["transformation_resilience_digital_twin"])

@router.get("", response_model=dict)
@router.get("/status", response_model=dict)
async def get_digital_twin_status():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    domains = overview.get("domains", [])
    if domains:
        return domains[0]
    return {"id": "dtdom_01", "name": "Digital Twin 2.0", "status": "current"}

@router.get("/current-state", response_model=dict)
async def get_digital_twin_current_state():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    states = overview.get("states", [])
    if states:
        return states[0]
    return {"id": "dtstate_01", "freshness": 1.0, "completeness": 0.98}

@router.get("/freshness", response_model=dict)
async def get_digital_twin_freshness():
    return {"freshness": 1.0, "event_lag_seconds": 0.0, "status": "fresh"}

@router.get("/completeness", response_model=dict)
async def get_digital_twin_completeness():
    return {"completeness": 0.98, "missing_objects_count": 0}

@router.get("/reality-comparison", response_model=List[dict])
async def get_reality_comparison():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("realityComparisons", [])

@router.get("/snapshots", response_model=List[dict])
async def list_snapshots():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("snapshots", [])

@router.post("/snapshots", response_model=dict)
async def create_snapshot():
    return {"id": "dtsnap_v2_1", "version": "v2.1", "status": "created"}

@router.get("/snapshots/{id}", response_model=dict)
async def get_snapshot(id: str):
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    for s in overview.get("snapshots", []):
        if s.get("id") == id or s.get("version") == id:
            return s
    return {"id": id, "version": "v2.0"}

@router.get("/snapshots/{id}/diff", response_model=List[dict])
async def get_snapshot_diff(id: str):
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("stateDiffs", [])

@router.post("/scenarios", response_model=dict)
async def create_scenario_fork(data: dict):
    base_id = data.get("base_snapshot_id", "dtsnap_v2_0")
    owner = data.get("owner", "Digital Twin Architect")
    return await TransformationResilienceDigitalTwinService.create_scenario_fork(None, base_id, owner)

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("counterfactualScenarios", [])

@router.get("/scenarios/{id}", response_model=dict)
async def get_scenario(id: str):
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    for cs in overview.get("counterfactualScenarios", []):
        if cs.get("id") == id:
            return cs
    return {"id": id, "horizon_days": 30}

@router.post("/scenarios/{id}/run", response_model=dict)
async def run_scenario(id: str):
    return await TransformationResilienceDigitalTwinService.run_what_if_analysis(None, [{"change_type": "dependency_failure"}])

@router.post("/what-if", response_model=dict)
async def run_what_if(data: dict):
    changes = data.get("changes", [])
    horizon = data.get("horizon_days", 30)
    return await TransformationResilienceDigitalTwinService.run_what_if_analysis(None, changes, horizon)

@router.post("/stress-tests", response_model=dict)
async def create_stress_test(data: dict):
    st_type = data.get("stress_type", "capacity_stress")
    sev = data.get("severity", "critical")
    return await TransformationResilienceDigitalTwinService.run_stress_test(None, st_type, sev)

@router.get("/stress-tests", response_model=List[dict])
async def list_stress_tests():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("stressScenarios", [])

@router.post("/recovery-scenarios", response_model=dict)
async def create_recovery_scenario(data: dict):
    mode = data.get("recovery_mode", "contingency_recovery")
    return await TransformationResilienceDigitalTwinService.run_recovery_simulation(None, mode)

@router.get("/recovery-scenarios", response_model=List[dict])
async def list_recovery_scenarios():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("recoveryScenarios", [])

@router.get("/experiments", response_model=List[dict])
async def list_experiments():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("experiments", [])

@router.post("/experiments", response_model=dict)
async def create_experiment(data: dict):
    return await TransformationResilienceDigitalTwinService.run_experiment(None, data)

@router.get("/experiments/{id}", response_model=dict)
async def get_experiment(id: str):
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    for ex in overview.get("experiments", []):
        if ex.get("id") == id:
            return ex
    return {"id": id, "title": "Governed Experiment"}

@router.post("/experiments/{id}/run", response_model=dict)
async def run_experiment_endpoint(id: str):
    return await TransformationResilienceDigitalTwinService.run_experiment(None, {"title": f"Experiment Run {id}"})

@router.get("/validation", response_model=List[dict])
async def get_validations():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("validations", [])

@router.get("/model-errors", response_model=List[dict])
async def get_model_errors():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("modelErrors", [])

@router.get("/drift", response_model=List[dict])
async def get_drifts():
    overview = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
    return overview.get("drifts", [])

@router.post("/query", response_model=TransformationResilienceDigitalTwinQueryResultRead)
async def process_digital_twin_query(query: str = Query(...)):
    return await TransformationResilienceDigitalTwinService.process_natural_language_digital_twin_query(None, query)
