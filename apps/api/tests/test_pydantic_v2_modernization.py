import pytest
from pydantic import ValidationError

from app.schemas.agent_runtime_v2 import (
    AgentExecutionCreate,
    AgentExecutionRead,
    AgentExecutionStateRead,
    AgentExecutionStepRead,
    ExecutionCheckpointRead,
    UnknownOutcomeRead,
    ExecutionTraceRead,
)
from app.schemas.capability_registry import (
    CapabilityCreate,
    CapabilityRead,
    CapabilityVersionRead,
    CapabilityInstallationRead,
    CapabilityHealthRead,
    CapabilityRequestRead,
    CapabilityPackageRead,
)
from app.schemas.control_plane import (
    OperationalHealthRead,
    ControlActionRead,
    ControlActionApprovalRead,
    OperationsOverviewRead,
)
from app.schemas.decision_engine import (
    DecisionRead,
    DecisionOptionRead,
    DecisionRiskRead,
    DecisionScenarioRead,
)
from app.schemas.enterprise_evaluation import (
    EvaluationRunRead,
    EvaluationDatasetRead,
    EvaluationCaseRead,
    EvaluationResultRead,
)
from app.schemas.event_mesh import (
    EventEnvelopeRead,
    EventSchemaRead,
    EventSubscriptionRead,
    EventDeliveryRead,
)
from app.schemas.intelligence_governance import (
    KnowledgeProvenanceRead,
    SourceAuthorityRead,
    KnowledgeClaimRead,
    AIOutputProvenanceRead,
)
from app.schemas.learning_fabric import (
    AgentMemoryRead,
    MemoryVersionRead,
    MemoryProvenanceRead,
    MemoryCandidateRead,
)
from app.schemas.mission_orchestration import (
    MissionObjectiveRead,
    MissionStepRead,
    MissionPlanRead,
    MissionCostRead,
)
from app.schemas.model_gateway import (
    ModelRegistryRead,
    ModelProviderRead,
    ModelRoutingDecisionRead,
    ModelHealthRead,
)
from app.schemas.policy_intelligence import (
    PolicyRead,
    PolicyVersionRead,
    RiskAssessmentRead,
    PolicyEvaluateResponse,
)
from app.schemas.semantic_graph import (
    SemanticEntityRead,
    SemanticRelationshipRead,
    RelationshipConflictRead,
    ContextPackRead,
)
from app.schemas.skill_fabric import (
    AgentSkillRead,
    AgentSkillVersionRead,
    SkillCandidateRead,
    SkillHealthRead,
)


def test_agent_runtime_v2_pydantic_v2_populate_by_name():
    # 1. Test creation by alias
    alias_payload = {
        "id": "exec_001",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "agentId": "agent_x",
        "missionId": "m_1",
        "workflowId": "w_1",
        "status": "RUNNING",
        "version": 1,
        "currentStep": "step_1",
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
    }
    exec_read = AgentExecutionRead.model_validate(alias_payload)
    assert exec_read.organization_id == "org_prime"
    assert exec_read.workspace_id == "ws_alpha"
    assert exec_read.agent_id == "agent_x"

    # 2. Test creation by field name (populate_by_name=True)
    field_payload = {
        "id": "exec_002",
        "organization_id": "org_prime",
        "workspace_id": "ws_alpha",
        "agent_id": "agent_x",
        "mission_id": "m_2",
        "workflow_id": "w_2",
        "status": "COMPLETED",
        "version": 2,
        "current_step": "step_final",
        "created_at": "2026-08-15T00:00:00Z",
        "updated_at": "2026-08-15T00:00:00Z",
    }
    exec_read_field = AgentExecutionRead.model_validate(field_payload)
    assert exec_read_field.organization_id == "org_prime"
    assert exec_read_field.current_step == "step_final"


def test_capability_registry_pydantic_v2():
    payload = {
        "id": "cap_001",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "ownerType": "workspace",
        "ownerId": "ws_alpha",
        "name": "data_extractor",
        "displayName": "Data Extractor Skill",
        "description": "Extracts structured data",
        "category": "analytics",
        "type": "skill",
        "status": "ACTIVE",
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
    }
    cap = CapabilityRead.model_validate(payload)
    assert cap.display_name == "Data Extractor Skill"
    assert cap.owner_type == "workspace"


def test_control_plane_pydantic_v2():
    payload = {
        "id": "act_01",
        "actionType": "RESTART_POD",
        "targetResource": "svc_api_gateway",
        "requestedBy": "admin_alex",
        "reason": "Routine failover recovery verification",
        "riskLevel": "LOW",
        "status": "COMPLETED",
        "idempotencyKey": "idem_001",
        "metadataInfo": {},
        "createdAt": "2026-08-15T00:00:00Z",
        "completedAt": "2026-08-15T00:01:00Z",
    }
    act = ControlActionRead.model_validate(payload)
    assert act.action_type == "RESTART_POD"
    assert act.target_resource == "svc_api_gateway"


def test_decision_engine_pydantic_v2_config_dict():
    payload = {
        "id": "dec_01",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "missionId": "mis_01",
        "agentId": "agent_alpha",
        "decisionType": "FAILOVER",
        "question": "Should we failover to region B?",
        "status": "APPROVED",
        "currentVersion": 1,
        "supersededBy": None,
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
    }
    dec = DecisionRead.model_validate(payload)
    assert dec.decision_type == "FAILOVER"
    assert dec.organization_id == "org_prime"


def test_enterprise_evaluation_pydantic_v2():
    payload = {
        "id": "run_01",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "evaluationType": "SECURITY",
        "targetType": "MODEL",
        "targetId": "mdl_01",
        "model": "claude-3-5-sonnet",
        "modelVersion": "20241022",
        "promptVersion": "v1.0",
        "contextVersion": "ctx_01",
        "status": "COMPLETED",
        "startedAt": "2026-08-15T00:00:00Z",
        "completedAt": "2026-08-15T00:01:00Z",
    }
    run = EvaluationRunRead.model_validate(payload)
    assert run.evaluation_type == "SECURITY"
    assert run.organization_id == "org_prime"


def test_event_mesh_and_semantic_graph_pydantic_v2():
    schema_payload = {
        "id": "sch_01",
        "eventType": "audit.login",
        "version": "1.0",
        "schemaJson": {"type": "object"},
        "producer": "auth-service",
        "status": "ACTIVE",
        "createdAt": "2026-08-15T00:00:00Z",
    }
    sch = EventSchemaRead.model_validate(schema_payload)
    assert sch.event_type == "audit.login"
    assert sch.version == "1.0"

    entity_payload = {
        "id": "ent_01",
        "entityId": "ent_01",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "entityType": "SERVICE",
        "displayName": "API Gateway Service",
        "status": "ACTIVE",
        "source": "k8s-cluster",
        "metadataInfo": {"region": "us-east-1"},
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
    }
    entity = SemanticEntityRead.model_validate(entity_payload)
    assert entity.entity_id == "ent_01"
    assert entity.display_name == "API Gateway Service"


def test_intelligence_governance_and_learning_fabric_pydantic_v2():
    claim_payload = {
        "id": "clm_01",
        "subject": "service_api",
        "predicate": "has_sla",
        "objectVal": "99.99%",
        "sourceReferences": [{"ref_id": "doc_ref_01"}],
        "status": "VERIFIED",
        "confidence": "HIGH",
        "observedAt": "2026-08-15T00:00:00Z",
    }
    claim = KnowledgeClaimRead.model_validate(claim_payload)
    assert claim.subject == "service_api"
    assert claim.confidence == "HIGH"

    mem_payload = {
        "id": "mem_01",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "ownerType": "AGENT",
        "ownerId": "agent_alpha",
        "memoryType": "EPISODIC",
        "scope": "SESSION",
        "title": "DB Failover Execution",
        "content": "User requested database trace",
        "status": "ACTIVE",
        "importance": "HIGH",
        "confidence": 0.99,
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
        "expiresAt": None,
    }
    mem = AgentMemoryRead.model_validate(mem_payload)
    assert mem.owner_id == "agent_alpha"
    assert mem.memory_type == "EPISODIC"


def test_mission_orchestration_model_gateway_skill_fabric_pydantic_v2():
    obj_payload = {
        "id": "obj_01",
        "missionId": "mis_01",
        "goal": "Perform database failover",
        "clarity": "HIGH",
        "constraints": {"loss_tolerance": "zero"},
        "successCriteria": ["RTO < 30s"],
        "priority": "HIGH",
        "deadline": None,
        "budgetUsd": None,
        "riskLevel": "LOW",
        "createdAt": "2026-08-15T00:00:00Z",
    }
    obj = MissionObjectiveRead.model_validate(obj_payload)
    assert obj.mission_id == "mis_01"
    assert obj.goal == "Perform database failover"

    prov_payload = {
        "id": "prv_01",
        "name": "Anthropic Claude",
        "providerKey": "anthropic",
        "status": "HEALTHY",
        "region": "us-east-1",
        "capabilities": ["chat", "streaming"],
        "createdAt": "2026-08-15T00:00:00Z",
    }
    prov = ModelProviderRead.model_validate(prov_payload)
    assert prov.provider_key == "anthropic"
    assert prov.status == "HEALTHY"

    skill_payload = {
        "id": "skl_01",
        "organizationId": "org_prime",
        "workspaceId": "ws_alpha",
        "ownerType": "SYSTEM",
        "ownerId": "sys_01",
        "name": "sql_generator",
        "description": "SQL Query Generator",
        "skillType": "DATABASE",
        "status": "ACTIVE",
        "currentVersionId": None,
        "createdAt": "2026-08-15T00:00:00Z",
        "updatedAt": "2026-08-15T00:00:00Z",
    }
    skill = AgentSkillRead.model_validate(skill_payload)
    assert skill.name == "sql_generator"
    assert skill.skill_type == "DATABASE"
