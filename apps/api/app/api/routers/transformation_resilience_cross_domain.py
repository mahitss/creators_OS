from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_cross_domain import (
    TransformationResilienceCrossDomainIntelligenceDomainRead,
    TransformationResilienceCrossDomainResilienceGraphRead,
    TransformationResilienceCrossDomainGraphNodeRead,
    TransformationResilienceCrossDomainGraphEdgeRead,
    TransformationResilienceCrossDomainPropagationPathRead,
    TransformationResilienceCrossDomainPropagationRead,
    TransformationResilienceCrossDomainSystemicExposureRead,
    TransformationResilienceCrossDomainConcentrationRead,
    TransformationResilienceCrossDomainSinglePointExposureRead,
    TransformationResilienceCrossDomainFragilityRead,
    TransformationResilienceCrossDomainRedundancyRead,
    TransformationResilienceCrossDomainResilienceGapRead,
    TransformationResilienceCrossDomainCompoundRiskRead,
    TransformationResilienceCrossDomainCompoundConditionRead,
    TransformationResilienceCrossDomainCascadeProjectionRead,
    TransformationResilienceCrossDomainCascadeBreakpointRead,
    TransformationResilienceCrossDomainSecondOrderEffectRead,
    TransformationResilienceCrossDomainInterventionCollisionRead,
    TransformationResilienceCrossDomainGovernanceContextRead,
    TransformationResilienceCrossDomainSystemicWarningRead,
    TransformationResilienceCrossDomainQueryResultRead
)
from app.services.transformation_resilience_cross_domain_service import TransformationResilienceCrossDomainService

router = APIRouter(prefix="/api/v1/transformation-resilience-cross-domain", tags=["transformation_resilience_cross_domain"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_cross_domain_overview():
    return await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)

@router.post("/query", response_model=TransformationResilienceCrossDomainQueryResultRead)
async def process_cross_domain_query(query: str = Query(...)):
    return await TransformationResilienceCrossDomainService.process_natural_language_cross_domain_query(None, query)

@router.get("/graph", response_model=dict)
async def get_resilience_graph():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    graphs = overview.get("resilienceGraphs", [])
    if graphs:
        return graphs[0]
    return {"id": "rgraph_01", "total_nodes_count": 12, "total_edges_count": 18, "status": "active"}

@router.get("/nodes", response_model=List[dict])
async def list_graph_nodes():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("nodes", [])

@router.get("/edges", response_model=List[dict])
async def list_graph_edges():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("edges", [])

@router.get("/exposures", response_model=List[dict])
async def list_systemic_exposures():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("systemicExposures", [])

@router.get("/propagation", response_model=List[dict])
async def list_propagations():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("propagations", [])

@router.get("/compound-risks", response_model=List[dict])
async def list_compound_risks():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("compoundRisks", [])

@router.get("/fragility", response_model=List[dict])
async def list_fragilities():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("fragilities", [])

@router.get("/redundancy", response_model=List[dict])
async def list_redundancies():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("redundancies", [])

@router.get("/gaps", response_model=List[dict])
async def list_resilience_gaps():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("resilienceGaps", [])

@router.get("/cascades", response_model=List[dict])
async def list_cascade_projections():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("cascadeProjections", [])

@router.get("/breakpoints", response_model=List[dict])
async def list_cascade_breakpoints():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("cascadeBreakpoints", [])

@router.get("/intervention-collisions", response_model=List[dict])
async def list_intervention_collisions():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("interventionCollisions", [])

@router.get("/graph/{nodeId}", response_model=dict)
async def get_graph_node(nodeId: str):
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    for n in overview.get("nodes", []):
        if n.get("id") == nodeId or n.get("node_id") == nodeId:
            return n
    return {"id": nodeId, "node_type": "dependency", "domain": "Infrastructure"}

@router.get("/graph/{nodeId}/dependents", response_model=List[dict])
async def get_node_dependents(nodeId: str):
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return [e for e in overview.get("edges", []) if e.get("target_node_id") == nodeId]

@router.get("/graph/{nodeId}/paths", response_model=List[dict])
async def get_node_paths(nodeId: str):
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("propagationPaths", [])

@router.post("/simulate", response_model=dict)
async def simulate_scenario(data: dict):
    return await TransformationResilienceCrossDomainService.simulate_cross_domain_scenario(None, data)

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    return [
        {"id": "xscen_01", "scenario_type": "single_dependency_failure", "risk_score": 0.88},
        {"id": "xscen_02", "scenario_type": "compound_risk", "risk_score": 0.94}
    ]

@router.get("/warnings", response_model=List[dict])
async def list_systemic_warnings():
    overview = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
    return overview.get("systemicWarnings", [])

@router.post("/graph/rebuild", response_model=dict)
async def rebuild_cross_domain_graph():
    return await TransformationResilienceCrossDomainService.rebuild_graph(None)
