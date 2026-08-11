from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.services.execution_governance_service import ExecutionGovernanceService
from app.schemas.execution_governance import (
    BenefitCreate, BenefitRead, BenefitEvidenceRead,
    ExecutionMilestoneCreate, ExecutionMilestoneRead,
    ExecutionVarianceRead, ExecutionGateRead, ExecutionChangeRequestRead,
    ExecutionForecastRead, ExecutionQueryResultRead
)

router = APIRouter(prefix="/execution", tags=["execution_governance_and_benefits_realization"])

@router.get("")
async def get_execution_overview():
    return await ExecutionGovernanceService.get_execution_overview(None)

@router.get("/benefits", response_model=List[BenefitRead])
async def get_benefits():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        BenefitRead(
            id=b["id"],
            organizationId=b["organization_id"],
            workspaceId=b["workspace_id"],
            portfolioId=b.get("portfolio_id"),
            programId=b.get("program_id"),
            initiativeId=b.get("initiative_id"),
            outcomeId=b.get("outcome_id"),
            name=b["name"],
            description=b["description"],
            owner=b["owner"],
            status=b["status"],
            benefitType=b["benefit_type"],
            baseline=b["baseline"],
            target=b["target"],
            currentValue=b["current_value"],
            unit=b["unit"],
            measurementMethod=b["measurement_method"],
            targetDate=b["target_date"],
            createdAt=b["created_at"],
            updatedAt=b["updated_at"]
        ) for b in ov["benefits"]
    ]

@router.post("/benefits", response_model=BenefitRead)
async def create_benefit(payload: BenefitCreate):
    b = await ExecutionGovernanceService.create_benefit(None, payload.model_dump())
    return BenefitRead(
        id=b["id"],
        organizationId=b["organization_id"],
        workspaceId=b["workspace_id"],
        portfolioId=b.get("portfolio_id"),
        programId=b.get("program_id"),
        initiativeId=b.get("initiative_id"),
        outcomeId=b.get("outcome_id"),
        name=b["name"],
        description=b["description"],
        owner=b["owner"],
        status=b["status"],
        benefitType=b["benefit_type"],
        baseline=b["baseline"],
        target=b["target"],
        currentValue=b["current_value"],
        unit=b["unit"],
        measurementMethod=b["measurement_method"],
        targetDate=b["target_date"],
        createdAt=b["created_at"],
        updatedAt=b["updated_at"]
    )

@router.get("/milestones", response_model=List[ExecutionMilestoneRead])
async def get_milestones():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        ExecutionMilestoneRead(
            id=m["id"],
            initiativeId=m["initiative_id"],
            name=m["name"],
            description=m["description"],
            dueDate=m["due_date"],
            status=m["status"],
            completionEvidence=m.get("completion_evidence")
        ) for m in ov["milestones"]
    ]

@router.get("/variances", response_model=List[ExecutionVarianceRead])
async def get_variances():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        ExecutionVarianceRead(
            id=v["id"],
            initiativeId=v["initiative_id"],
            varianceType=v["variance_type"],
            baseline=v["baseline"],
            actual=v["actual"],
            forecast=v["forecast"],
            delta=v["delta"],
            severity=v["severity"]
        ) for v in ov["variances"]
    ]

@router.get("/gates", response_model=List[ExecutionGateRead])
async def get_gates():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        ExecutionGateRead(
            id=g["id"],
            initiativeId=g["initiative_id"],
            gateType=g["gate_type"],
            status=g["status"],
            waiverActor=g.get("waiver_actor"),
            waiverReason=g.get("waiver_reason")
        ) for g in ov["gates"]
    ]

@router.get("/change-requests", response_model=List[ExecutionChangeRequestRead])
async def get_change_requests():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        ExecutionChangeRequestRead(
            id=cr["id"],
            initiativeId=cr["initiative_id"],
            changeType=cr["change_type"],
            requestedChange=cr["requested_change"],
            reason=cr["reason"],
            impactSummary=cr["impact_summary"],
            status=cr["status"],
            requester=cr["requester"]
        ) for cr in ov["changeRequests"]
    ]

@router.get("/forecasts", response_model=List[ExecutionForecastRead])
async def get_forecasts():
    ov = await ExecutionGovernanceService.get_execution_overview(None)
    return [
        ExecutionForecastRead(
            id=fc["id"],
            initiativeId=fc["initiative_id"],
            forecastCompletionDate=fc["forecast_completion_date"],
            forecastCost=fc["forecast_cost"],
            forecastBenefit=fc["forecast_benefit"],
            lowerBound=fc["lower_bound"],
            upperBound=fc["upper_bound"],
            confidencePct=fc["confidence_pct"]
        ) for fc in ov["forecasts"]
    ]

@router.post("/query", response_model=ExecutionQueryResultRead)
async def query_execution(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await ExecutionGovernanceService.process_natural_language_execution_query(None, q)
    return ExecutionQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )
