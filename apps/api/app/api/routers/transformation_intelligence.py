from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_intelligence import (
    TransformationGraphNodeRead,
    TransformationGraphEdgeRead,
    TransformationGraphProvenanceRead,
    TransformationImpactMapRead,
    CrossTransformationImpactRead,
    TransformationCapabilityOverlapRead,
    TransformationAssumptionClusterRead,
    TransformationScenarioExposureRead,
    TransformationBenefitGraphRead,
    TransformationConflictGraphRead,
    TransformationPatternRead,
    TransformationAnalogyRead,
    TransformationComplexityHotspotRead,
    TransformationGraphSnapshotRead,
    TransformationQueryResultRead
)
from app.services.transformation_intelligence_service import TransformationIntelligenceService

router = APIRouter(prefix="/api/v1/transformation-intelligence", tags=["transformation_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_fabric_overview():
    return await TransformationIntelligenceService.get_fabric_overview(None)

@router.get("/graph", response_model=dict)
async def get_graph():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return {"nodes": overview.get("nodes", []), "edges": overview.get("edges", [])}

@router.get("/graph/nodes", response_model=List[dict])
async def list_nodes():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("nodes", [])

@router.get("/graph/edges", response_model=List[dict])
async def list_edges():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("edges", [])

@router.get("/graph/paths", response_model=dict)
async def get_paths(from_entity: str = Query("cand_01"), to_entity: str = Query("cand_02")):
    return await TransformationIntelligenceService.query_multi_hop_paths(None, from_entity, to_entity)

@router.get("/capability-overlaps", response_model=List[dict])
async def list_capability_overlaps():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("capabilityOverlaps", [])

@router.get("/assumption-clusters", response_model=List[dict])
async def list_assumption_clusters():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("assumptionClusters", [])

@router.get("/scenario-exposure", response_model=List[dict])
async def list_scenario_exposures():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("scenarioExposures", [])

@router.get("/benefit-overlaps", response_model=List[dict])
async def list_benefit_overlaps():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("benefitGraphs", [])

@router.get("/patterns", response_model=List[dict])
async def list_patterns():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("patterns", [])

@router.get("/analogies", response_model=List[dict])
async def list_analogies():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("analogies", [])

@router.get("/hotspots", response_model=List[dict])
async def list_hotspots():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("hotspots", [])

@router.get("/snapshots", response_model=List[dict])
async def list_snapshots():
    overview = await TransformationIntelligenceService.get_fabric_overview(None)
    return overview.get("snapshots", [])

@router.post("/query", response_model=TransformationQueryResultRead)
async def process_intelligence_query(query: str = Query(...)):
    return await TransformationIntelligenceService.process_natural_language_intelligence_query(None, query)
