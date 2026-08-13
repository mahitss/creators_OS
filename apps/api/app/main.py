from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.errors import VaporException, ErrorCode
from app.middleware.request_logging import RequestLoggingMiddleware
from app.api.routers import health, auth, workspace, home, missions, memories, content, deliverables, attention, search, integrations, calendar, gmail, drive, agent_runs, evaluations, admin_agents, policies, delegations, automations, insights, workflows, workflow_ai, finops, infrastructure, reliability, governance, identity, scim, dlp, knowledge, agent_mesh, decision_intelligence, workflow_optimization, events, operations, graph, knowledge_governance, enterprise_evaluation, model_gateway, agent_runtime_v2, learning_fabric, skill_fabric, capability_registry, mission_orchestration, decision_engine, governance_v2, security, secops, resilience, finops_v2, collaboration_v2, operating_graph, strategic_planning, portfolio_intelligence, execution_governance, performance_intelligence, predictive_operations, prescriptive_intelligence, adaptive_decision_governance, continuity_intelligence, crisis_intelligence, threat_intelligence, foresight_intelligence, adaptive_strategy, execution_intelligence, operating_model, transformation, transformation_portfolio, transformation_control, transformation_intelligence, transformation_foresight, transformation_decisions, transformation_decision_learning, transformation_governance, transformation_simulation, transformation_war_room, transformation_recovery, transformation_resilience_engineering, transformation_resilience_portfolio, transformation_resilience_sensing, transformation_resilience_command_center, transformation_resilience_decision_lifecycle, transformation_resilience_decision_learning

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Standardized Exception Handler for VaporException
@app.exception_handler(VaporException)
async def vapor_exception_handler(request: Request, exc: VaporException):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "request_id": request_id,
            "path": str(request.url.path),
            "details": exc.details
        }
    )

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": ErrorCode.INTERNAL_ERROR,
            "message": "An unexpected error occurred on the Vapor core API.",
            "request_id": request_id,
            "path": str(request.url.path)
        }
    )

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
app.include_router(workspace.router, prefix=settings.API_V1_STR, tags=["Workspace"])
app.include_router(home.router, prefix=settings.API_V1_STR, tags=["Home"])
app.include_router(missions.router, prefix=settings.API_V1_STR, tags=["Missions"])
app.include_router(memories.router, prefix=settings.API_V1_STR, tags=["Memories"])
app.include_router(content.router, prefix=settings.API_V1_STR, tags=["Content"])
app.include_router(deliverables.router, prefix=settings.API_V1_STR, tags=["Deliverables"])
app.include_router(attention.router, prefix=settings.API_V1_STR, tags=["Attention"])
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["Search"])
app.include_router(integrations.router, prefix=settings.API_V1_STR, tags=["Integrations"])
app.include_router(calendar.router, prefix=settings.API_V1_STR, tags=["Calendar"])
app.include_router(gmail.router, prefix=settings.API_V1_STR, tags=["Gmail"])
app.include_router(drive.router, prefix=settings.API_V1_STR, tags=["Drive"])
app.include_router(agent_runs.router, prefix=settings.API_V1_STR, tags=["Agent Runs"])
app.include_router(evaluations.router, prefix=settings.API_V1_STR, tags=["Evaluations"])
app.include_router(admin_agents.router, prefix=settings.API_V1_STR, tags=["Admin Agents"])
app.include_router(policies.router, prefix=settings.API_V1_STR, tags=["Policies"])
app.include_router(agent_mesh.router, prefix=settings.API_V1_STR, tags=["AI Agent Mesh & Multi-Agent Orchestration"])
app.include_router(delegations.router, prefix=settings.API_V1_STR, tags=["Delegations"])
app.include_router(automations.router, prefix=settings.API_V1_STR, tags=["Automations"])
app.include_router(insights.router, prefix=settings.API_V1_STR, tags=["Insights"])
app.include_router(workflow_optimization.router, prefix=settings.API_V1_STR, tags=["Adaptive Workflow Intelligence & Self-Optimizing Automation"])
app.include_router(workflows.router, prefix=settings.API_V1_STR, tags=["Workflows"])
app.include_router(workflow_ai.router, prefix=settings.API_V1_STR, tags=["AI Workflow Intelligence"])
app.include_router(finops.router, prefix=settings.API_V1_STR, tags=["FinOps"])
app.include_router(infrastructure.router, prefix=settings.API_V1_STR, tags=["Infrastructure"])
app.include_router(reliability.router, prefix=settings.API_V1_STR, tags=["Reliability & Self-Healing"])
app.include_router(governance.router, prefix=settings.API_V1_STR, tags=["Enterprise Governance & Compliance"])
app.include_router(identity.router, prefix=settings.API_V1_STR, tags=["Enterprise Identity & SSO"])
app.include_router(scim.router, tags=["SCIM 2.0 Provisioning"])
app.include_router(dlp.router, prefix=settings.API_V1_STR, tags=["Data Security & DLP"])
app.include_router(knowledge.router, prefix=settings.API_V1_STR, tags=["Knowledge Fabric & Secure AI Retrieval"])
app.include_router(decision_intelligence.router, prefix=settings.API_V1_STR, tags=["Enterprise Decision Intelligence & Predictive Operations"])
app.include_router(events.router, prefix=settings.API_V1_STR, tags=["Enterprise Event Mesh & Real-Time Intelligence Fabric"])
app.include_router(operations.router, prefix=settings.API_V1_STR, tags=["Enterprise Control Plane & Global Operations Center"])
app.include_router(graph.router, prefix=settings.API_V1_STR, tags=["Enterprise Semantic Graph & Unified Business Context"])
app.include_router(knowledge_governance.router, prefix=settings.API_V1_STR, tags=["Enterprise Intelligence Governance & Trusted Knowledge Fabric"])
app.include_router(enterprise_evaluation.router, prefix=settings.API_V1_STR, tags=["Enterprise AI Evaluation & Continuous Intelligence Improvement"])
app.include_router(model_gateway.router, prefix=settings.API_V1_STR, tags=["Enterprise AI Model Gateway & Intelligent Model Routing"])
app.include_router(agent_runtime_v2.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Runtime 2.0 & Durable Cognitive Execution"])
app.include_router(learning_fabric.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Memory & Learning Fabric"])
app.include_router(skill_fabric.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Skill Fabric & Controlled Skill Evolution"])
app.include_router(capability_registry.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Capability Registry & Skill Marketplace Foundation"])
app.include_router(mission_orchestration.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Orchestration & Mission Intelligence 2.0"])
app.include_router(decision_engine.router, prefix=settings.API_V1_STR, tags=["Enterprise Decision Intelligence 2.0 & Evidence-Backed Agent Decision Engine"])
app.include_router(governance_v2.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Governance & Policy Intelligence 2.0"])
app.include_router(security.router, prefix=settings.API_V1_STR, tags=["Enterprise Agent Security & Threat Intelligence Fabric"])
app.include_router(secops.router, prefix=settings.API_V1_STR, tags=["Enterprise AI Security Operations & Controlled Incident Response"])
app.include_router(resilience.router, prefix=settings.API_V1_STR, tags=["Enterprise AI Resilience & Business Continuity Fabric"])
app.include_router(finops_v2.router, prefix=settings.API_V1_STR, tags=["Enterprise AI FinOps & Capacity Intelligence 2.0"])
app.include_router(collaboration_v2.router, prefix=settings.API_V1_STR, tags=["Enterprise Human-AI Collaboration & Workforce Intelligence 2.0"])
app.include_router(operating_graph.router, prefix=settings.API_V1_STR, tags=["Enterprise Organizational Intelligence & Operating Graph 2.0"])
app.include_router(strategic_planning.router, prefix=settings.API_V1_STR, tags=["Enterprise Strategic Planning & Scenario Intelligence 2.0"])
app.include_router(portfolio_intelligence.router, prefix=settings.API_V1_STR, tags=["Enterprise Portfolio Intelligence & Investment Optimization 2.0"])
app.include_router(execution_governance.router, prefix=settings.API_V1_STR, tags=["Enterprise Execution Governance & Benefits Realization 2.0"])
app.include_router(performance_intelligence.router, prefix=settings.API_V1_STR, tags=["Enterprise Performance Intelligence & KPI Operating System 2.0"])
app.include_router(predictive_operations.router, prefix=settings.API_V1_STR, tags=["Enterprise Predictive Operations & Forecast Intelligence 2.0"])
app.include_router(execution_intelligence.router, prefix=settings.API_V1_STR, tags=["Enterprise Strategic Execution Intelligence 2.0"])
app.include_router(operating_model.router, prefix=settings.API_V1_STR, tags=["Enterprise Organizational Operating Intelligence 2.0"])
app.include_router(transformation.router, prefix=settings.API_V1_STR, tags=["Enterprise Operating Model Transformation 2.0"])
app.include_router(transformation_portfolio.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Portfolio Intelligence 2.0"])
app.include_router(transformation_control.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Control Tower 2.0"])
app.include_router(transformation_intelligence.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Intelligence Fabric 2.0"])
app.include_router(transformation_foresight.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Foresight 2.0"])
app.include_router(transformation_decisions.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Decision Intelligence 3.0"])
app.include_router(transformation_decision_learning.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Decision Lifecycle & Closed-Loop Decision Learning 2.0"])
app.include_router(transformation_governance.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Adaptive Governance 2.0"])
app.include_router(transformation_simulation.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Governance Digital Twin & Multi-Layer Simulation 2.0"])
app.include_router(transformation_war_room.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation War Room 2.0"])
app.include_router(transformation_recovery.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Recovery 2.0"])
app.include_router(transformation_resilience_engineering.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Engineering 2.0"])
app.include_router(transformation_resilience_portfolio.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Portfolio 2.0"])
app.include_router(transformation_resilience_sensing.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Sensing 2.0"])
app.include_router(transformation_resilience_command_center.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Command Center 2.0"])
app.include_router(transformation_resilience_decision_lifecycle.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Decision Lifecycle 2.0"])
app.include_router(transformation_resilience_decision_learning.router, prefix=settings.API_V1_STR, tags=["Enterprise Transformation Resilience Decision Learning 2.0"])






@app.get("/")
async def root():
    return {
        "message": "Vapor OS Core Kernel API",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
