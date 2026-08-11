from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.security_fabric_service import SecurityFabricService
from app.schemas.security import (
    SecurityEventCreate, SecurityEventRead,
    ThreatFindingRead, SecurityIncidentCreate, SecurityIncidentRead,
    SecurityQuarantineCreate, SecurityQuarantineRead,
    AgentBehaviorBaselineRead, BehaviorAnomalyRead,
    ThreatIntelligenceSignalCreate, ThreatIntelligenceSignalRead
)

router = APIRouter(prefix="/security", tags=["security"])

@router.get("/events", response_model=List[SecurityEventRead])
async def get_security_events(
    org_id: str = Query("org_default_creator", alias="orgId"),
    limit: int = 50
):
    evts = await SecurityFabricService.get_events(None, org_id, limit)
    return [
        SecurityEventRead(
            id=e["id"],
            organizationId=e["organization_id"],
            workspaceId=e["workspace_id"],
            eventType=e["event_type"],
            severity=e["severity"],
            source=e["source"],
            actor=e["actor"],
            resource=e["resource"],
            missionId=e.get("mission_id"),
            agentId=e.get("agent_id"),
            timestamp=e["timestamp"],
            status=e["status"]
        ) for e in evts
    ]

@router.get("/events/{event_id}", response_model=SecurityEventRead)
async def get_security_event_detail(event_id: str):
    evts = await SecurityFabricService.get_events(None, "org_default_creator", 100)
    for e in evts:
        if e["id"] == event_id:
            return SecurityEventRead(
                id=e["id"],
                organizationId=e["organization_id"],
                workspaceId=e["workspace_id"],
                eventType=e["event_type"],
                severity=e["severity"],
                source=e["source"],
                actor=e["actor"],
                resource=e["resource"],
                missionId=e.get("mission_id"),
                agentId=e.get("agent_id"),
                timestamp=e["timestamp"],
                status=e["status"]
            )
    raise HTTPException(status_code=404, detail=f"Security event '{event_id}' not found.")

@router.get("/threats", response_model=List[ThreatFindingRead])
async def get_threat_findings(status: Optional[str] = None):
    threats = await SecurityFabricService.get_threats(None, status)
    return [
        ThreatFindingRead(
            id=t["id"],
            securityEventId=t["security_event_id"],
            threatType=t["threat_type"],
            severity=t["severity"],
            status=t["status"],
            evidence=t["evidence"],
            recommendedAction=t["recommended_action"]
        ) for t in threats
    ]

@router.get("/threats/{threat_id}", response_model=ThreatFindingRead)
async def get_threat_finding_detail(threat_id: str):
    threats = await SecurityFabricService.get_threats(None)
    for t in threats:
        if t["id"] == threat_id:
            return ThreatFindingRead(
                id=t["id"],
                securityEventId=t["security_event_id"],
                threatType=t["threat_type"],
                severity=t["severity"],
                status=t["status"],
                evidence=t["evidence"],
                recommendedAction=t["recommended_action"]
            )
    raise HTTPException(status_code=404, detail=f"Threat finding '{threat_id}' not found.")

@router.get("/incidents", response_model=List[SecurityIncidentRead])
async def get_security_incidents(org_id: str = Query("org_default_creator", alias="orgId")):
    incidents = await SecurityFabricService.get_incidents(None, org_id)
    return [
        SecurityIncidentRead(
            id=i["id"],
            organizationId=i["organization_id"],
            severity=i["severity"],
            status=i["status"],
            summary=i["summary"],
            createdAt=i["created_at"],
            resolvedAt=i.get("resolved_at")
        ) for i in incidents
    ]

@router.post("/incidents", response_model=SecurityIncidentRead)
async def create_security_incident(payload: SecurityIncidentCreate):
    inc = await SecurityFabricService.create_incident(None, payload.model_dump())
    return SecurityIncidentRead(
        id=inc["id"],
        organizationId=inc["organization_id"],
        severity=inc["severity"],
        status=inc["status"],
        summary=inc["summary"],
        createdAt=inc["created_at"],
        resolvedAt=inc.get("resolved_at")
    )

@router.get("/incidents/{incident_id}", response_model=SecurityIncidentRead)
async def get_security_incident_detail(incident_id: str):
    incidents = await SecurityFabricService.get_incidents(None, "org_default_creator")
    for i in incidents:
        if i["id"] == incident_id:
            return SecurityIncidentRead(
                id=i["id"],
                organizationId=i["organization_id"],
                severity=i["severity"],
                status=i["status"],
                summary=i["summary"],
                createdAt=i["created_at"],
                resolvedAt=i.get("resolved_at")
            )
    raise HTTPException(status_code=404, detail=f"Security incident '{incident_id}' not found.")

@router.post("/incidents/{incident_id}/contain")
async def contain_incident(incident_id: str):
    incidents = await SecurityFabricService.get_incidents(None, "org_default_creator")
    for i in incidents:
        if i["id"] == incident_id:
            i["status"] = "contained"
            return {"status": "success", "incident_id": incident_id, "state": "contained"}
    raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

@router.post("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str):
    incidents = await SecurityFabricService.get_incidents(None, "org_default_creator")
    for i in incidents:
        if i["id"] == incident_id:
            i["status"] = "resolved"
            return {"status": "success", "incident_id": incident_id, "state": "resolved"}
    raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

@router.post("/incidents/{incident_id}/close")
async def close_incident(incident_id: str):
    incidents = await SecurityFabricService.get_incidents(None, "org_default_creator")
    for i in incidents:
        if i["id"] == incident_id:
            i["status"] = "closed"
            return {"status": "success", "incident_id": incident_id, "state": "closed"}
    raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

@router.get("/investigations")
async def get_investigations():
    return {"investigations": []}

@router.post("/investigations")
async def create_investigation(payload: Dict[str, Any]):
    return {
        "id": "inv_demo_01",
        "incident_id": payload.get("incidentId", "inc_demo_01"),
        "investigator_id": payload.get("investigatorId", "sec_analyst_01"),
        "status": "active",
        "timeline": []
    }

@router.get("/quarantine", response_model=List[SecurityQuarantineRead])
async def get_quarantines(status: str = "active"):
    qs = await SecurityFabricService.get_quarantines(None, status)
    return [
        SecurityQuarantineRead(
            id=q["id"],
            targetType=q["target_type"],
            targetId=q["target_id"],
            reason=q["reason"],
            scope=q["scope"],
            createdBy=q["created_by"],
            expiresAt=q.get("expires_at"),
            releasePolicy=q["release_policy"],
            status=q["status"]
        ) for q in qs
    ]

@router.post("/quarantine", response_model=SecurityQuarantineRead)
async def create_quarantine(payload: SecurityQuarantineCreate):
    q = await SecurityFabricService.quarantine_target(None, payload.model_dump())
    return SecurityQuarantineRead(
        id=q["id"],
        targetType=q["target_type"],
        targetId=q["target_id"],
        reason=q["reason"],
        scope=q["scope"],
        createdBy=q["created_by"],
        expiresAt=q.get("expires_at"),
        releasePolicy=q["release_policy"],
        status=q["status"]
    )

@router.post("/quarantine/{quarantine_id}/release", response_model=SecurityQuarantineRead)
async def release_quarantine_endpoint(quarantine_id: str, release_by: str = Query("sec_admin")):
    q = await SecurityFabricService.release_quarantine(None, quarantine_id, release_by)
    if not q:
        raise HTTPException(status_code=404, detail=f"Quarantine '{quarantine_id}' not found.")
    return SecurityQuarantineRead(
        id=q["id"],
        targetType=q["target_type"],
        targetId=q["target_id"],
        reason=q["reason"],
        scope=q["scope"],
        createdBy=q["created_by"],
        expiresAt=q.get("expires_at"),
        releasePolicy=q["release_policy"],
        status=q["status"]
    )

@router.get("/agents/{agent_id}/baseline", response_model=AgentBehaviorBaselineRead)
async def get_agent_baseline(agent_id: str):
    b = await SecurityFabricService.get_agent_baseline(None, agent_id)
    return AgentBehaviorBaselineRead(
        id=b["id"],
        organizationId=b["organization_id"],
        workspaceId=b["workspace_id"],
        agentId=b["agent_id"],
        toolFrequencyJson=b["tool_frequency_json"],
        avgLatencyMs=b["avg_latency_ms"],
        avgDataVolumeBytes=b["avg_data_volume_bytes"],
        createdAt=b["created_at"],
        updatedAt=b["updated_at"]
    )

@router.get("/agents/{agent_id}/anomalies", response_model=List[BehaviorAnomalyRead])
async def get_agent_anomalies(agent_id: str):
    anomalies = await SecurityFabricService.get_agent_anomalies(None, agent_id)
    return [
        BehaviorAnomalyRead(
            id=a["id"],
            agentId=a["agent_id"],
            anomalyType=a["anomaly_type"],
            deviationScore=a["deviation_score"],
            evidence=a["evidence"],
            createdAt=a["created_at"]
        ) for a in anomalies
    ]

@router.get("/intelligence", response_model=List[ThreatIntelligenceSignalRead])
async def get_threat_intelligence():
    signals = await SecurityFabricService.get_threat_intel(None)
    return [
        ThreatIntelligenceSignalRead(
            id=s["id"],
            source=s["source"],
            confidence=s["confidence"],
            freshness=s["freshness"],
            indicatorType=s["indicator_type"],
            indicatorValue=s["indicator_value"],
            context=s["context"],
            createdAt=s["created_at"]
        ) for s in signals
    ]

@router.post("/intelligence/signals", response_model=ThreatIntelligenceSignalRead)
async def add_threat_intelligence_signal(payload: ThreatIntelligenceSignalCreate):
    s = await SecurityFabricService.add_intel_signal(None, payload.model_dump())
    return ThreatIntelligenceSignalRead(
        id=s["id"],
        source=s["source"],
        confidence=s["confidence"],
        freshness=s["freshness"],
        indicatorType=s["indicator_type"],
        indicatorValue=s["indicator_value"],
        context=s["context"],
        createdAt=s["created_at"]
    )
