import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_intervention_domains: Dict[str, dict] = {}
_in_memory_intervention_cases: Dict[str, dict] = {}
_in_memory_intervention_triggers: Dict[str, dict] = {}
_in_memory_intervention_options: Dict[str, dict] = {}
_in_memory_rollback_plans: Dict[str, dict] = {}
_in_memory_contingency_plans: Dict[str, dict] = {}
_in_memory_contingency_readinesses: Dict[str, dict] = {}
_in_memory_intervention_recommendations: Dict[str, dict] = {}
_in_memory_intervention_decision_packets: Dict[str, dict] = {}
_in_memory_intervention_plans: Dict[str, dict] = {}
_in_memory_intervention_actions: Dict[str, dict] = {}
_in_memory_intervention_expirations: Dict[str, dict] = {}
_in_memory_intervention_conflicts: Dict[str, dict] = {}
_in_memory_intervention_cascades: Dict[str, dict] = {}
_in_memory_intervention_impacts: Dict[str, dict] = {}
_in_memory_intervention_effectivenesses: Dict[str, dict] = {}
_in_memory_intervention_failures: Dict[str, dict] = {}
_in_memory_intervention_lessons: Dict[str, dict] = {}

_EMITTED_INTERVENTION_EVENTS: List[dict] = []

EMITTED_INTERVENTION_EVENT_TYPES = [
    "transformation.resilience.assurance.intervention.domain.created",
    "transformation.resilience.assurance.intervention.trigger.detected",
    "transformation.resilience.assurance.intervention.trigger.validated",
    "transformation.resilience.assurance.intervention.case.created",
    "transformation.resilience.assurance.intervention.option.created",
    "transformation.resilience.assurance.intervention.scenario.created",
    "transformation.resilience.assurance.intervention.recommendation.created",
    "transformation.resilience.assurance.intervention.decision_packet.created",
    "transformation.resilience.assurance.intervention.decision.created",
    "transformation.resilience.assurance.intervention.approval.requested",
    "transformation.resilience.assurance.intervention.approved",
    "transformation.resilience.assurance.intervention.plan.created",
    "transformation.resilience.assurance.intervention.action.ready",
    "transformation.resilience.assurance.intervention.action.started",
    "transformation.resilience.assurance.intervention.action.completed",
    "transformation.resilience.assurance.intervention.action.failed",
    "transformation.resilience.assurance.intervention.rollback.started",
    "transformation.resilience.assurance.intervention.rollback.completed",
    "transformation.resilience.assurance.intervention.contingency.created",
    "transformation.resilience.assurance.intervention.contingency.activated",
    "transformation.resilience.assurance.intervention.readiness.updated",
    "transformation.resilience.assurance.intervention.conflict.detected",
    "transformation.resilience.assurance.intervention.cascade.detected",
    "transformation.resilience.assurance.intervention.expired",
    "transformation.resilience.assurance.intervention.stale",
    "transformation.resilience.assurance.intervention.effectiveness.updated",
    "transformation.resilience.assurance.intervention.failure.detected",
    "transformation.resilience.assurance.intervention.lesson.created"
]

def _initialize_seed_assurance_interventions_data():
    if _in_memory_intervention_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    expires_iso = (now + timedelta(days=14)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Intervention Domain
    idom1 = {
        "id": "idom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Assurance Intervention Orchestration 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Assurance Intervention Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_intervention_domains[idom1["id"]] = idom1

    # Intervention Case & Trigger
    icase1 = {
        "id": "icase_01",
        "warning_id": "ewarn_01",
        "forecast_id": "fcst_01",
        "risk_id": "emrisk_01",
        "affected_plans_json": ["aplan_01", "aplan_hr_cloud_02"],
        "affected_transformations_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
        "severity": "high",
        "horizon": "near_term",
        "intervention_window": "10 days remaining",
        "status": "options_ready",
        "owner": "Transformation Resilience Preventive Operations Engineer",
        "created_at": now_iso
    }
    _in_memory_intervention_cases[icase1["id"]] = icase1

    itrig1 = {
        "id": "itrig_01",
        "type": "early_warning",
        "signal_id": "fsig_01",
        "evidence_description": "Gradual 15% increase in Simulation Cluster 01 queue depth over past 14 days.",
        "confidence": 0.95,
        "freshness": 0.98,
        "threshold_value": 0.85,
        "validation_status": "validated"
    }
    _in_memory_intervention_triggers[itrig1["id"]] = itrig1

    # Intervention Options (Includes mandatory baseline 'continue_current_state')
    iopt_base = {
        "id": "iopt_baseline_01",
        "case_id": icase1["id"],
        "option_type": "continue_current_state",
        "title": "Baseline Option: Continue Current State / Do Nothing",
        "reversibility": "reversible",
        "risk_reduction": 0.0,
        "coverage": 0.84,
        "effort": "none",
        "capacity_required": "0 compute nodes",
        "residual_risk": 0.25,
        "created_at": now_iso
    }
    _in_memory_intervention_options[iopt_base["id"]] = iopt_base

    iopt_reseq = {
        "id": "iopt_resequence_01",
        "case_id": icase1["id"],
        "option_type": "resequence",
        "title": "Preemptive Resequencing Option (Stagger simulation runs by 7 days)",
        "reversibility": "reversible",
        "risk_reduction": 0.90,
        "coverage": 0.92,
        "effort": "medium",
        "capacity_required": "0 additional nodes (shifts load profile)",
        "residual_risk": 0.08,
        "created_at": now_iso
    }
    _in_memory_intervention_options[iopt_reseq["id"]] = iopt_reseq

    iopt_reserve = {
        "id": "iopt_reserve_01",
        "case_id": icase1["id"],
        "option_type": "reserve_capacity",
        "title": "Capacity Expansion Option (Reserve 4 cloud compute nodes)",
        "reversibility": "partially_reversible",
        "risk_reduction": 0.95,
        "coverage": 0.95,
        "effort": "high",
        "capacity_required": "4 compute nodes",
        "residual_risk": 0.05,
        "created_at": now_iso
    }
    _in_memory_intervention_options[iopt_reserve["id"]] = iopt_reserve

    # Rollback Plan & Contingency Plan
    rplan1 = {
        "id": "rplan_01",
        "option_id": iopt_reseq["id"],
        "rollback_trigger": "Simulated capacity bottleneck is cleared earlier than week 3.",
        "rollback_actions_json": ["Restore original simulation schedule", "Notify cloud ops team"],
        "authorization_required": "Governance Board Authorization",
        "expected_recovery_time_hours": 2,
        "residual_risk": 0.05,
        "created_at": now_iso
    }
    _in_memory_rollback_plans[rplan1["id"]] = rplan1

    cplan1 = {
        "id": "cplan_01",
        "case_id": icase1["id"],
        "activation_criteria": "If queue depth exceeds 90% in week 2.",
        "actions_json": ["Activate burst cloud capacity node pool"],
        "owners_json": ["Cloud Infrastructure Lead"],
        "capacity_reserved": "2 backup compute nodes",
        "status": "ready"
    }
    _in_memory_contingency_plans[cplan1["id"]] = cplan1

    cread1 = {
        "id": "cread_01",
        "contingency_id": cplan1["id"],
        "evidence_readiness": "ready",
        "resource_readiness": "ready",
        "dependency_readiness": "partially_ready",
        "execution_readiness": "ready",
        "governance_readiness": "ready",
        "overall_status": "partially_ready",
        "created_at": now_iso
    }
    _in_memory_contingency_readinesses[cread1["id"]] = cread1

    # Recommendation, Decision Packet, Intervention Plan, Action
    irec1 = {
        "id": "irec_01",
        "case_id": icase1["id"],
        "label": "ANALYTICAL RECOMMENDATION — NOT DECISION",
        "recommended_option_id": iopt_reseq["id"],
        "reason": "Preemptive resequencing eliminates predicted compute bottleneck with zero budget increase and high reversibility.",
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_intervention_recommendations[irec1["id"]] = irec1

    dpack1 = {
        "id": "dpack_01",
        "case_id": icase1["id"],
        "governance_requirement": "Requires Governance Board sign-off prior to week 2 close.",
        "packet_summary": "Intervention Decision Packet for Q3 Wave 4 Compute Deficit Risk.",
        "created_at": now_iso
    }
    _in_memory_intervention_decision_packets[dpack1["id"]] = dpack1

    iplan1 = {
        "id": "iplan_01",
        "case_id": icase1["id"],
        "objective": "Eliminate Q3 Wave 4 simulation compute bottleneck",
        "selected_option_id": iopt_reseq["id"],
        "status": "approved"
    }
    _in_memory_intervention_plans[iplan1["id"]] = iplan1

    iact1 = {
        "id": "iact_01",
        "plan_id": iplan1["id"],
        "action_type": "change_sequence",
        "description": "Shift HR Cloud Wave 4 simulation batch by 7 days.",
        "status": "ready"
    }
    _in_memory_intervention_actions[iact1["id"]] = iact1

    # Expirations, Conflicts, Cascades, Impacts, Effectiveness, Failures, Lessons
    iexp1 = {
        "id": "iexp_01",
        "case_id": icase1["id"],
        "reason": "Intervention window closes at week 2 close.",
        "expires_at": expires_iso
    }
    _in_memory_intervention_expirations[iexp1["id"]] = iexp1

    iconf1 = {
        "id": "iconf_01",
        "case_id": icase1["id"],
        "conflicting_plan_id": "aplan_hr_cloud_02",
        "severity": "high",
        "conflict_summary": "Resequencing shifts simulation batch into HR Cloud testing window."
    }
    _in_memory_intervention_conflicts[iconf1["id"]] = iconf1

    icasc1 = {
        "id": "icasc_01",
        "source_action_id": iact1["id"],
        "affected_plan_id": "aplan_hr_cloud_02",
        "severity": "material",
        "confidence": 0.92
    }
    _in_memory_intervention_cascades[icasc1["id"]] = icasc1

    iimp1 = {
        "id": "iimp_01",
        "case_id": icase1["id"],
        "risk_reduction": 0.90,
        "coverage_change": 0.08,
        "capacity_impact": "Shifted load by 7 days",
        "residual_risk": 0.08,
        "created_at": now_iso
    }
    _in_memory_intervention_impacts[iimp1["id"]] = iimp1

    ieff1 = {
        "id": "ieff_01",
        "case_id": icase1["id"],
        "lead_time_days": 14.0,
        "risk_reduction": 0.90,
        "coverage_preservation": 0.92,
        "rollback_success": True,
        "created_at": now_iso
    }
    _in_memory_intervention_effectivenesses[ieff1["id"]] = ieff1

    ifail1 = {
        "id": "ifail_01",
        "case_id": "icase_legacy_00",
        "failure_type": "execution_failure",
        "description": "Simulation queue clearing failed during wave 1 deployment due to cloud API network timeout.",
        "cause": "Transient DNS resolution error on legacy endpoint."
    }
    _in_memory_intervention_failures[ifail1["id"]] = ifail1

    iless1 = {
        "id": "iless_01",
        "lesson_type": "timing",
        "title": "Intervention Timing Lesson",
        "description": "Submitting intervention decision packets 10 days in advance allows full governance approval without delaying wave deployment.",
        "created_at": now_iso
    }
    _in_memory_intervention_lessons[iless1["id"]] = iless1

_initialize_seed_assurance_interventions_data()


class TransformationResilienceAssuranceInterventionsService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_INTERVENTION_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may validate warnings, prepare options, run simulations, prepare intervention plans, prepare rollback plans, monitor execution, detect stale interventions, detect intervention conflicts
        # Agents may NOT approve, accept material risk, activate irreversible interventions without authorization, change budgets, allocate employees, or override PolicyEngine
        forbidden_actions = [
            "approve", "accept_material_risk", "activate_irreversible_intervention",
            "change_budgets", "allocate_employees", "override_policy_engine"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing action '{action}'. Decision authority belongs strictly to human governance."
            }
        return {"allowed": True, "reason": "Action permitted for assurance intervention agent."}

    @staticmethod
    async def get_assurance_interventions_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_assurance_interventions_data()
        domains = list(_in_memory_intervention_domains.values())
        cases = list(_in_memory_intervention_cases.values())
        triggers = list(_in_memory_intervention_triggers.values())
        options = list(_in_memory_intervention_options.values())
        rollbacks = list(_in_memory_rollback_plans.values())
        contingencies = list(_in_memory_contingency_plans.values())
        readinesses = list(_in_memory_contingency_readinesses.values())
        recommendations = list(_in_memory_intervention_recommendations.values())
        decision_packets = list(_in_memory_intervention_decision_packets.values())
        plans = list(_in_memory_intervention_plans.values())
        actions = list(_in_memory_intervention_actions.values())
        expirations = list(_in_memory_intervention_expirations.values())
        conflicts = list(_in_memory_intervention_conflicts.values())
        cascades = list(_in_memory_intervention_cascades.values())
        impacts = list(_in_memory_intervention_impacts.values())
        effectivenesses = list(_in_memory_intervention_effectivenesses.values())
        failures = list(_in_memory_intervention_failures.values())
        lessons = list(_in_memory_intervention_lessons.values())

        return {
            "domainsCount": len(domains),
            "casesCount": len(cases),
            "triggersCount": len(triggers),
            "optionsCount": len(options),
            "rollbacksCount": len(rollbacks),
            "contingenciesCount": len(contingencies),
            "plansCount": len(plans),
            "actionsCount": len(actions),
            "conflictsCount": len(conflicts),
            "lessonsCount": len(lessons),
            "domains": domains,
            "cases": cases,
            "triggers": triggers,
            "options": options,
            "rollbackPlans": rollbacks,
            "contingencyPlans": contingencies,
            "readinesses": readinesses,
            "recommendations": recommendations,
            "decisionPackets": decision_packets,
            "plans": plans,
            "actions": actions,
            "expirations": expirations,
            "conflicts": conflicts,
            "cascades": cascades,
            "impacts": impacts,
            "effectivenesses": effectivenesses,
            "failures": failures,
            "lessons": lessons
        }

    @staticmethod
    async def simulate_intervention_scenario(session: Optional[AsyncSession], case_id: str, data: dict) -> dict:
        _initialize_seed_assurance_interventions_data()
        scen_id = f"iscen_{uuid.uuid4().hex[:8]}"
        scen = {
            "id": scen_id,
            "case_id": case_id,
            "scenario_type": data.get("scenario_type", "resequence"),
            "risk_reduction": 0.90,
            "coverage_score": 0.92,
            "residual_risk": 0.08,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        TransformationResilienceAssuranceInterventionsService.emit_event(
            "transformation.resilience.assurance.intervention.scenario.created", scen
        )
        return scen

    @staticmethod
    async def request_intervention_approval(session: Optional[AsyncSession], case_id: str) -> dict:
        _initialize_seed_assurance_interventions_data()
        icase = _in_memory_intervention_cases.get(case_id)
        if not icase:
            return {"error": "Intervention case not found."}

        icase["status"] = "awaiting_decision"
        TransformationResilienceAssuranceInterventionsService.emit_event(
            "transformation.resilience.assurance.intervention.approval.requested",
            {"case_id": case_id, "status": "awaiting_decision"}
        )
        return {"case_id": case_id, "status": "awaiting_decision"}

    @staticmethod
    async def execute_intervention_action(session: Optional[AsyncSession], action_id: str) -> dict:
        _initialize_seed_assurance_interventions_data()
        act = _in_memory_intervention_actions.get(action_id)
        if not act:
            return {"error": "Intervention action not found."}

        act["status"] = "completed"
        TransformationResilienceAssuranceInterventionsService.emit_event(
            "transformation.resilience.assurance.intervention.action.completed",
            {"action_id": action_id, "status": "completed"}
        )
        return {"action_id": action_id, "status": "completed"}

    @staticmethod
    async def process_natural_language_assurance_intervention_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_assurance_interventions_data()

        # Anti-Surveillance / Privacy check (blocking employee intervention scores, individual employee risk forecasts, or worker productivity predictions)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee intervention score", "individual employee risk forecast", "worker productivity prediction",
            "score employee intervention", "surveil worker intervention"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee intervention scores, individual employee risk forecasts, or worker productivity predictions."},
                "confidencePct": 0.0
            }

        # Enforce DLP checks
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Enforce Multi-Tenant Isolation
        if caller_org_id != "org_global_enterprise_01":
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "DENY. Organization tenant isolation breach detected."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "intervention_cases": "Active Intervention Case 'icase_01' (Options Ready, High Severity): Q3 Wave 4 Simulation Compute Deficit Risk affecting plans 'aplan_01' and 'aplan_hr_cloud_02'.",
                    "triggers": "Trigger 'itrig_01' (Early Warning, Validated): Queue depth threshold crossing (85% threshold, 95% confidence).",
                    "intervention_options": "Intervention Options: Baseline 'Continue Current State' (Risk 0.25, Coverage 84%) vs Option 'Preemptive Resequencing' (Risk Reduction 90%, Reversible, Residual Risk 0.08) vs Option 'Capacity Expansion' (Reversibility: Partially Reversible).",
                    "rollback_plans": "Rollback Plan 'rplan_01': Triggered if bottleneck clears earlier than week 3 (Authorization: Governance Board, Recovery: 2 hours).",
                    "contingencies_and_readiness": "Contingency Plan 'cplan_01' (Status: Ready, Readiness: Partially Ready): Activate burst cloud capacity pool if queue depth exceeds 90%.",
                    "recommendation_notice": "ANALYTICAL RECOMMENDATION — NOT DECISION. Preemptive resequencing eliminates compute bottleneck with high reversibility.",
                    "governance_and_execution": "Decision Packet 'dpack_01' requires Governance Board approval prior to week 2 close. ActionGateway protects action execution.",
                    "effectiveness_and_learning": "Intervention Effectiveness 'ieff_01': 14 days lead time, 90% risk reduction, 92% coverage preservation, rollback success."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Assurance Intervention Orchestration Engine 2.0",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
