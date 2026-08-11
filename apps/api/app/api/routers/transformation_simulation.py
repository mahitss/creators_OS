from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_simulation import (
    TransformationDigitalTwinRead,
    TransformationTwinBaselineRead,
    TransformationTwinSnapshotRead,
    TransformationSimulationRunRead,
    TransformationSimulationOutputRead,
    TransformationMultiScenarioRunRead,
    TransformationSimulationComparisonRead,
    TransformationSimulationTradeoffRead,
    TransformationSensitivityAnalysisRead,
    TransformationSimulationReviewRead,
    TransformationWhatIfQueryResultRead
)
from app.services.transformation_simulation_service import TransformationSimulationService

router = APIRouter(prefix="/api/v1/transformation-simulation", tags=["transformation_simulation"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_simulation_overview():
    return await TransformationSimulationService.get_simulation_overview(None)

@router.get("/twins", response_model=List[dict])
async def list_digital_twins():
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return overview.get("twins", [])

@router.post("/twins", response_model=dict)
async def create_digital_twin(data: dict):
    return {"id": "twin_new", "name": data.get("name", "New Digital Twin"), "status": "active", "version": "v2.0"}

@router.get("/twins/{id}", response_model=dict)
async def get_digital_twin(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    for t in overview.get("twins", []):
        if t.get("id") == id:
            return t
    return {"id": id, "name": "Global Digital Twin", "status": "active"}

@router.get("/twins/{id}/snapshots", response_model=List[dict])
async def list_twin_snapshots(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return [s for s in overview.get("snapshots", []) if s.get("twin_id") == id or id == "twin_01"]

@router.get("/runs", response_model=List[dict])
async def list_simulation_runs():
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return overview.get("runs", [])

@router.post("/runs", response_model=dict)
async def create_simulation_run(data: dict):
    return {"id": "sim_run_new", "status": "completed", "hash_fingerprint": "sim_fingerprint_hash_9999"}

@router.get("/runs/{id}", response_model=dict)
async def get_simulation_run(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    for r in overview.get("runs", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "completed"}

@router.post("/runs/{id}/cancel", response_model=dict)
async def cancel_simulation_run(id: str):
    return {"id": id, "status": "cancelled"}

@router.get("/runs/{id}/outputs", response_model=List[dict])
async def get_run_outputs(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return [o for o in overview.get("outputs", []) if o.get("run_id") == id or id == "sim_run_01"]

@router.post("/what-if", response_model=dict)
async def execute_what_if_query(data: dict):
    return await TransformationSimulationService.process_natural_language_what_if_query(None, data.get("query", "What if Wave 2 is delayed?"))

@router.get("/what-if/{id}", response_model=dict)
async def get_what_if_result(id: str):
    return {"id": id, "query": "What if Wave 2 is delayed?", "status": "completed"}

@router.post("/what-if/{id}/compare", response_model=dict)
async def compare_what_if_states(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return overview.get("comparisons", [{}])[0]

@router.get("/runs/{id}/sensitivity", response_model=List[dict])
async def get_run_sensitivity(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return overview.get("sensitivityAnalyses", [])

@router.get("/runs/{id}/thresholds", response_model=dict)
async def get_run_thresholds(id: str):
    return {"runId": id, "capacityThresholdExceeded": False, "governanceLoadThresholdPct": 78.5}

@router.get("/runs/{id}/robustness", response_model=dict)
async def get_run_robustness(id: str):
    return {"runId": id, "robustnessScore": 0.92, "fragilityWarnings": ["Single dependency bottleneck on Core IAM integration"]}

@router.get("/runs/{id}/fragility", response_model=dict)
async def get_run_fragility(id: str):
    return {"runId": id, "fragilityWarnings": ["Single dependency bottleneck on Core IAM integration"]}

@router.get("/runs/{id}/calibration", response_model=dict)
async def get_run_calibration(id: str):
    return {"runId": id, "calibrationPct": 95.8, "historicalError": 0.042}

@router.get("/reviews", response_model=List[dict])
async def list_simulation_reviews():
    overview = await TransformationSimulationService.get_simulation_overview(None)
    return overview.get("reviews", [])

@router.post("/reviews", response_model=dict)
async def create_simulation_review(data: dict):
    return {"id": "sim_rev_new", "status": "approved"}

@router.get("/reviews/{id}", response_model=dict)
async def get_simulation_review(id: str):
    overview = await TransformationSimulationService.get_simulation_overview(None)
    for r in overview.get("reviews", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "approved"}

@router.post("/reviews/{id}/complete", response_model=dict)
async def complete_simulation_review(id: str):
    return {"id": id, "status": "completed"}

@router.post("/query", response_model=TransformationWhatIfQueryResultRead)
async def process_what_if_query(query: str = Query(...)):
    return await TransformationSimulationService.process_natural_language_what_if_query(None, query)
