from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.operating_graph_service import OperatingGraphService
from app.schemas.operating_graph import (
    OutcomeCreate, OutcomeRead, OperatingChangeEventRead,
    OperatingScenarioCreate, OperatingScenarioRead, OperatingRiskRead,
    CapabilityGapRead, OperatingBottleneckRead, OperatingDependencyRead,
    GraphValidationIssueRead, GraphQueryResultRead
)

router = APIRouter(prefix="/organization", tags=["operating_graph_and_organizational_intelligence"])

@router.get("")
async def get_organization_overview():
    return await OperatingGraphService.get_organization_overview(None)

@router.get("/outcomes", response_model=List[OutcomeRead])
async def get_outcomes():
    ov = await OperatingGraphService.get_organization_overview(None)
    return [
        OutcomeRead(
            id=o["id"],
            organizationId=o["organization_id"],
            workspaceId=o["workspace_id"],
            name=o["name"],
            description=o["description"],
            owner=o["owner"],
            status=o["status"],
            target=o["target"],
            currentState=o["current_state"],
            createdAt=o["created_at"],
            updatedAt=o["updated_at"]
        ) for o in ov["outcomes"]
    ]

@router.post("/outcomes", response_model=OutcomeRead)
async def create_outcome(payload: OutcomeCreate):
    o = await OperatingGraphService.create_outcome(None, payload.model_dump())
    return OutcomeRead(
        id=o["id"],
        organizationId=o["organization_id"],
        workspaceId=o["workspace_id"],
        name=o["name"],
        description=o["description"],
        owner=o["owner"],
        status=o["status"],
        target=o["target"],
        currentState=o["current_state"],
        createdAt=o["created_at"],
        updatedAt=o["updated_at"]
    )

@router.get("/risks", response_model=List[OperatingRiskRead])
async def get_risks():
    ov = await OperatingGraphService.get_organization_overview(None)
    return [
        OperatingRiskRead(
            id=r["id"],
            organizationId=r["organization_id"],
            dimension=r["dimension"],
            title=r["title"],
            description=r["description"],
            sourceRef=r["source_ref"],
            evidenceJson=r["evidence_json"],
            status=r["status"],
            mitigationRecommendationsJson=r["mitigation_recommendations_json"],
            createdAt=r["created_at"]
        ) for r in ov["risks"]
    ]

@router.get("/bottlenecks", response_model=List[OperatingBottleneckRead])
async def get_bottlenecks():
    ov = await OperatingGraphService.get_organization_overview(None)
    return [
        OperatingBottleneckRead(
            id=b["id"],
            organizationId=b["organization_id"],
            blockerType=b["blocker_type"],
            rootDependencyRef=b["root_dependency_ref"],
            affectedWorkJson=b["affected_work_json"],
            durationHours=b["duration_hours"],
            evidenceJson=b["evidence_json"],
            status=b["status"],
            createdAt=b["created_at"]
        ) for b in ov["bottlenecks"]
    ]

@router.get("/capabilities", response_model=List[CapabilityGapRead])
async def get_capability_gaps():
    ov = await OperatingGraphService.get_organization_overview(None)
    return [
        CapabilityGapRead(
            id=g["id"],
            organizationId=g["organization_id"],
            capabilityId=g["capability_id"],
            requiredByRef=g["required_by_ref"],
            gapClassification=g["gap_classification"],
            impactSummary=g["impact_summary"],
            status=g["status"],
            createdAt=g["created_at"]
        ) for g in ov["gaps"]
    ]

@router.get("/graph")
async def get_operating_graph():
    return {
        "nodes": [
            {"id": "org_01", "type": "Organization", "label": "Vapor OS Enterprise"},
            {"id": "team_core", "type": "Team", "label": "Core Infrastructure Team"},
            {"id": "mis_analysis_99", "type": "Mission", "label": "Q3 Financial Data Analysis"},
            {"id": "out_01", "type": "Outcome", "label": "SOC2 Compliance Certification"}
        ],
        "edges": [
            {"source": "team_core", "target": "mis_analysis_99", "type": "OWNS"},
            {"source": "mis_analysis_99", "target": "out_01", "type": "RESULTS_IN"}
        ]
    }

@router.post("/query", response_model=GraphQueryResultRead)
async def query_operating_graph(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await OperatingGraphService.process_natural_language_query(None, q)
    return GraphQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )

@router.post("/scenarios", response_model=OperatingScenarioRead)
async def create_scenario(payload: OperatingScenarioCreate):
    s = await OperatingGraphService.simulate_scenario(None, payload.model_dump())
    return OperatingScenarioRead(
        id=s["id"],
        organizationId=s["organization_id"],
        name=s["name"],
        assumptionsJson=s["assumptions_json"],
        affectedNodesJson=s["affected_nodes_json"],
        expectedImpactJson=s["expected_impact_json"],
        confidencePct=s["confidence_pct"],
        createdAt=s["created_at"]
    )

@router.post("/scenarios/{sc_id}/simulate", response_model=OperatingScenarioRead)
async def simulate_existing_scenario(sc_id: str):
    s = await OperatingGraphService.simulate_scenario(None, {"name": f"Scenario {sc_id}"})
    return OperatingScenarioRead(
        id=s["id"],
        organizationId=s["organization_id"],
        name=s["name"],
        assumptionsJson=s["assumptions_json"],
        affectedNodesJson=s["affected_nodes_json"],
        expectedImpactJson=s["expected_impact_json"],
        confidencePct=s["confidence_pct"],
        createdAt=s["created_at"]
    )
