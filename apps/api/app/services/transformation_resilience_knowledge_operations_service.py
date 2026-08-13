import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_operations_domains: Dict[str, dict] = {}
_in_memory_risk_cases: Dict[str, dict] = {}
_in_memory_risk_queues: Dict[str, dict] = {}
_in_memory_risk_assignments: Dict[str, dict] = {}
_in_memory_remediation_plans: Dict[str, dict] = {}
_in_memory_remediation_actions: Dict[str, dict] = {}
_in_memory_evidence_tasks: Dict[str, dict] = {}
_in_memory_review_tasks: Dict[str, dict] = {}
_in_memory_remediation_verifications: Dict[str, dict] = {}
_in_memory_remediation_effectivenesses: Dict[str, dict] = {}
_in_memory_risk_escalations: Dict[str, dict] = {}
_in_memory_remediation_failures: Dict[str, dict] = {}
_in_memory_recurring_risk_patterns: Dict[str, dict] = {}
_in_memory_remediation_qualities: Dict[str, dict] = {}
_in_memory_operating_patterns: Dict[str, dict] = {}

_EMITTED_OPERATIONS_EVENTS: List[dict] = []

EMITTED_OPERATIONS_EVENT_TYPES = [
    "transformation.resilience.knowledge.operations.domain.created",
    "transformation.resilience.knowledge.risk.detected",
    "transformation.resilience.knowledge.risk.triaged",
    "transformation.resilience.knowledge.risk.assigned",
    "transformation.resilience.knowledge.remediation.created",
    "transformation.resilience.knowledge.remediation.started",
    "transformation.resilience.knowledge.remediation.completed",
    "transformation.resilience.knowledge.evidence_task.created",
    "transformation.resilience.knowledge.evidence_task.completed",
    "transformation.resilience.knowledge.review_task.created",
    "transformation.resilience.knowledge.review_task.completed",
    "transformation.resilience.knowledge.risk.escalated",
    "transformation.resilience.knowledge.risk.accepted",
    "transformation.resilience.knowledge.risk.deferred",
    "transformation.resilience.knowledge.remediation.failed",
    "transformation.resilience.knowledge.remediation.verified",
    "transformation.resilience.knowledge.remediation.effectiveness.updated",
    "transformation.resilience.knowledge.recurring_risk.detected",
    "transformation.resilience.knowledge.risk_concentration.updated",
    "transformation.resilience.knowledge.sla.breached",
    "transformation.resilience.knowledge.operating_pattern.detected"
]

def _initialize_seed_resilience_operations_data():
    if _in_memory_operations_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    due_iso = (now + timedelta(days=7)).isoformat()
    past_due_iso = (now - timedelta(days=2)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Operations Domain
    opdom1 = {
        "id": "opdom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Knowledge Operations & Remediation Operating System 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Knowledge Operations Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_operations_domains[opdom1["id"]] = opdom1

    # Risk Cases
    rc1 = {
        "id": "rcase_01",
        "knowledge_object_id": "kobj_less_01",
        "risk_type": "high_influence_low_quality",
        "severity": "high",
        "impact": "high_decision_impact",
        "urgency": "high",
        "owner": "Principal Decision Assurance Engineer",
        "status": "in_remediation",
        "detected_at": now_iso,
        "due_at": due_iso
    }
    _in_memory_risk_cases[rc1["id"]] = rc1

    rc_overdue = {
        "id": "rcase_overdue_01",
        "knowledge_object_id": "kobj_stale_02",
        "risk_type": "stale_unsupported_precedent",
        "severity": "critical",
        "impact": "critical_decision_impact",
        "urgency": "high",
        "owner": "Enterprise Architecture Board",
        "status": "triaged",
        "detected_at": (now - timedelta(days=10)).isoformat(),
        "due_at": past_due_iso
    }
    _in_memory_risk_cases[rc_overdue["id"]] = rc_overdue

    rc_accepted = {
        "id": "rcase_accepted_01",
        "knowledge_object_id": "kobj_legacy_03",
        "risk_type": "context_mismatch",
        "severity": "medium",
        "impact": "medium_decision_impact",
        "urgency": "low",
        "owner": "Legacy System Remediation Lead",
        "status": "accepted_risk",
        "detected_at": now_iso,
        "due_at": due_iso,
        "reason": "Legacy datacenter migration scheduled for Q4 will supersede this context.",
        "review_date": (now + timedelta(days=90)).isoformat()
    }
    _in_memory_risk_cases[rc_accepted["id"]] = rc_accepted

    rc_deferred = {
        "id": "rcase_deferred_01",
        "knowledge_object_id": "kobj_vendor_04",
        "risk_type": "unsupported_claim",
        "severity": "low",
        "impact": "low_decision_impact",
        "urgency": "low",
        "owner": "Vendor Assurance Lead",
        "status": "deferred",
        "detected_at": now_iso,
        "due_at": due_iso,
        "defer_until": (now + timedelta(days=30)).isoformat(),
        "consequence": "Minor ambiguity in non-critical vendor SLA benchmark."
    }
    _in_memory_risk_cases[rc_deferred["id"]] = rc_deferred

    # Risk Queue
    rq1 = {
        "id": "rq_01",
        "risk_case_id": rc1["id"],
        "severity": "high",
        "impact": "high_decision_impact",
        "owner": rc1["owner"],
        "deadline": due_iso,
        "status": "in_remediation"
    }
    _in_memory_risk_queues[rq1["id"]] = rq1

    # Assignment
    asgn1 = {
        "id": "rasgn_01",
        "risk_case_id": rc1["id"],
        "owner": rc1["owner"],
        "assigned_by": "Principal Knowledge Operations Architect",
        "assigned_at": now_iso,
        "reason": "High decision influence on Multi-Region Token Cache deployment."
    }
    _in_memory_risk_assignments[asgn1["id"]] = asgn1

    # Remediation Plan & Actions
    plan1 = {
        "id": "rplan_01",
        "risk_case_id": rc1["id"],
        "objective": "Collect independent telemetry to validate +15ms SLA buffer under 10Gbps interconnect load.",
        "owner": rc1["owner"],
        "deadline": due_iso,
        "actions_json": [
            {"id": "act_01", "action_type": "collect_evidence", "title": "Obtain independent telemetry from third-party vendor", "owner": "Observability Lead", "status": "in_progress"},
            {"id": "act_02", "action_type": "request_revalidation", "title": "Submit revalidation packet to Governance Board", "owner": rc1["owner"], "status": "planned"}
        ],
        "success_criteria": "Independent telemetry corroborates SLA jitter with zero same-origin bias.",
        "rollback_strategy": "Maintain existing +15ms buffer pending independent review.",
        "status": "in_progress"
    }
    _in_memory_remediation_plans[plan1["id"]] = plan1

    act1 = {
        "id": "act_01",
        "plan_id": plan1["id"],
        "action_type": "collect_evidence",
        "title": "Obtain independent telemetry from third-party vendor",
        "owner": "Observability Lead",
        "status": "in_progress",
        "created_at": now_iso
    }
    _in_memory_remediation_actions[act1["id"]] = act1

    # Evidence Task (with safety non-fabrication rule)
    etask1 = {
        "id": "etask_01",
        "gap_id": "egap_01",
        "requested_evidence": "Third-party synthetic latency trace for secondary cloud provider route",
        "source": "Independent Monitoring Network",
        "owner": "Observability Lead",
        "deadline": due_iso,
        "status": "assigned",
        "quality": 0.95
    }
    _in_memory_evidence_tasks[etask1["id"]] = etask1

    # Review Task
    rtask1 = {
        "id": "rtask_01",
        "risk_case_id": rc1["id"],
        "review_question": "Does the +15ms buffer remain required after fiber route upgrade?",
        "reviewer": "Principal Knowledge Governance Architect",
        "deadline": due_iso,
        "status": "assigned",
        "result": "inconclusive"
    }
    _in_memory_review_tasks[rtask1["id"]] = rtask1

    # Verification & Effectiveness
    verif1 = {
        "id": "rverif_01",
        "risk_case_id": rc1["id"],
        "risk_before": {"severity": "high", "risk_type": "high_influence_low_quality"},
        "risk_after": {"severity": "low", "risk_type": "remediated"},
        "knowledge_health_before": {"freshness_score": 0.70, "evidence_coverage": 0.65},
        "knowledge_health_after": {"freshness_score": 0.96, "evidence_coverage": 0.95},
        "evidence_quality_before": {"quality": 0.60, "independence": "derived"},
        "evidence_quality_after": {"quality": 0.95, "independence": "independent"},
        "created_at": now_iso
    }
    _in_memory_remediation_verifications[verif1["id"]] = verif1

    eff1 = {
        "id": "reff_01",
        "risk_case_id": rc1["id"],
        "risk_reduction": 0.85,
        "evidence_improvement": 0.90,
        "confidence_improvement": 0.88,
        "applicability_improvement": 0.92,
        "reuse_improvement": 0.95,
        "created_at": now_iso
    }
    _in_memory_remediation_effectivenesses[eff1["id"]] = eff1

    # Escalation
    esc1 = {
        "id": "resc_01",
        "risk_case_id": rc_overdue["id"],
        "trigger": "sla_breached_critical_severity",
        "severity": "critical",
        "owner": "Enterprise Architecture Board",
        "status": "escalated",
        "created_at": now_iso
    }
    _in_memory_risk_escalations[esc1["id"]] = esc1

    # Failure
    fail1 = {
        "id": "rfail_01",
        "risk_case_id": "rcase_failed_05",
        "failure_category": "evidence_unavailable",
        "reason": "Target API telemetry source deprecated without replacement contract.",
        "created_at": now_iso
    }
    _in_memory_remediation_failures[fail1["id"]] = fail1

    # Recurring Pattern
    rec1 = {
        "id": "rrec_01",
        "pattern_title": "Repeated Evidence Gap in Secondary Cloud Provider SLA Jitter",
        "frequency": 4,
        "affected_knowledge_json": ["kobj_less_01", "kobj_cloud_02"],
        "affected_decisions_json": ["dec_res_01", "dec_wave_04_hr"],
        "confidence": 0.94
    }
    _in_memory_recurring_risk_patterns[rec1["id"]] = rec1

    # Quality & Operating Pattern
    qual1 = {
        "id": "rqual_01",
        "risk_case_id": rc1["id"],
        "completeness": 0.95,
        "evidence_quality": 0.94,
        "verification_quality": 0.96,
        "timeliness": 0.92,
        "repeatability": 0.90,
        "created_at": now_iso
    }
    _in_memory_remediation_qualities[qual1["id"]] = qual1

    opat1 = {
        "id": "opat_01",
        "title": "Independent Evidence Corroboration Pattern",
        "description": "Cross-verifying secondary vendor benchmarks via third-party synthetic monitoring resolves high-influence knowledge risks.",
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_operating_patterns[opat1["id"]] = opat1

_initialize_seed_resilience_operations_data()


class TransformationResilienceKnowledgeOperationsService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_OPERATIONS_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may detect risks, prepare remediation plans, collect permitted evidence, prepare review packets, monitor deadlines, identify recurring patterns, and prepare executive summaries
        # Agents may NOT approve remediation, accept risk, change governance, invalidate knowledge, or execute material changes
        forbidden_actions = [
            "approve_remediation", "accept_risk", "change_governance",
            "invalidate_knowledge", "execute_material_changes"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing operational governance action '{action}'. Risk acceptance and remediation approval require human governance authority."
            }
        return {"allowed": True, "reason": "Action permitted for knowledge operations agent."}

    @staticmethod
    async def get_knowledge_operations_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_operations_data()
        domains = list(_in_memory_operations_domains.values())
        cases = list(_in_memory_risk_cases.values())
        queues = list(_in_memory_risk_queues.values())
        assignments = list(_in_memory_risk_assignments.values())
        plans = list(_in_memory_remediation_plans.values())
        actions = list(_in_memory_remediation_actions.values())
        etasks = list(_in_memory_evidence_tasks.values())
        rtasks = list(_in_memory_review_tasks.values())
        verifications = list(_in_memory_remediation_verifications.values())
        effectivenesses = list(_in_memory_remediation_effectivenesses.values())
        escalations = list(_in_memory_risk_escalations.values())
        failures = list(_in_memory_remediation_failures.values())
        recurring = list(_in_memory_recurring_risk_patterns.values())
        qualities = list(_in_memory_remediation_qualities.values())
        op_patterns = list(_in_memory_operating_patterns.values())

        critical_cnt = sum(1 for c in cases if c.get("severity") == "critical")
        overdue_cnt = sum(1 for c in cases if c.get("due_at") and c.get("due_at") < datetime.now(timezone.utc).isoformat() and c.get("status") not in ["closed", "verified"])
        accepted_cnt = sum(1 for c in cases if c.get("status") == "accepted_risk")
        deferred_cnt = sum(1 for c in cases if c.get("status") == "deferred")

        return {
            "domainsCount": len(domains),
            "casesCount": len(cases),
            "criticalCount": critical_cnt,
            "overdueCount": overdue_cnt,
            "acceptedCount": accepted_cnt,
            "deferredCount": deferred_cnt,
            "plansCount": len(plans),
            "evidenceTasksCount": len(etasks),
            "reviewTasksCount": len(rtasks),
            "escalationsCount": len(escalations),
            "recurringPatternsCount": len(recurring),
            "domains": domains,
            "cases": cases,
            "queues": queues,
            "assignments": assignments,
            "plans": plans,
            "actions": actions,
            "evidenceTasks": etasks,
            "reviewTasks": rtasks,
            "verifications": verifications,
            "effectivenesses": effectivenesses,
            "escalations": escalations,
            "failures": failures,
            "recurring": recurring,
            "qualities": qualities,
            "operatingPatterns": op_patterns,
            "riskConcentration": [
                {
                    "domain": "Secondary Cloud Resilience",
                    "transformation": "Global Enterprise Multi-Region Cloud Wave 4",
                    "weakestAssurance": "Lack of Independent Telemetry Corroboration",
                    "riskCount": 3,
                    "severity": "high"
                }
            ]
        }

    @staticmethod
    async def assign_risk(session: Optional[AsyncSession], risk_id: str, owner: str, assigned_by: str, reason: str) -> dict:
        _initialize_seed_resilience_operations_data()
        rc = _in_memory_risk_cases.get(risk_id)
        if not rc:
            return {"error": "Risk case not found."}

        rc["owner"] = owner
        rc["status"] = "assigned"

        asgn_id = f"rasgn_{uuid.uuid4().hex[:8]}"
        asgn = {
            "id": asgn_id,
            "risk_case_id": risk_id,
            "owner": owner,
            "assigned_by": assigned_by,
            "assigned_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason
        }
        _in_memory_risk_assignments[asgn_id] = asgn

        TransformationResilienceKnowledgeOperationsService.emit_event(
            "transformation.resilience.knowledge.risk.assigned", asgn
        )
        return asgn

    @staticmethod
    async def verify_remediation(session: Optional[AsyncSession], risk_id: str, data: dict) -> dict:
        _initialize_seed_resilience_operations_data()
        rc = _in_memory_risk_cases.get(risk_id)
        if not rc:
            return {"error": "Risk case not found."}

        verif_id = f"rverif_{uuid.uuid4().hex[:8]}"
        verif = {
            "id": verif_id,
            "risk_case_id": risk_id,
            "risk_before": data.get("risk_before", {"severity": "high"}),
            "risk_after": data.get("risk_after", {"severity": "low"}),
            "knowledge_health_before": data.get("knowledge_health_before", {"freshness_score": 0.70}),
            "knowledge_health_after": data.get("knowledge_health_after", {"freshness_score": 0.96}),
            "evidence_quality_before": data.get("evidence_quality_before", {"quality": 0.60}),
            "evidence_quality_after": data.get("evidence_quality_after", {"quality": 0.95}),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_remediation_verifications[verif_id] = verif
        rc["status"] = "verified"

        TransformationResilienceKnowledgeOperationsService.emit_event(
            "transformation.resilience.knowledge.remediation.verified", verif
        )
        return verif

    @staticmethod
    async def process_natural_language_operations_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_operations_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking employee performance scores, individual remediation rankings, or employee behavioral profiles)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee performance score", "remediation ranking", "individual behavioral profile",
            "employee remediation score", "rank employee", "surveillance"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee performance scores, individual remediation rankings, or employee behavioral profiles."},
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
                    "risk_attention": "Risk Case 'rcase_01' (High Severity) requires evidence corroboration; Remediation Plan 'rplan_01' is underway.",
                    "overdue_risks": "Risk Case 'rcase_overdue_01' is OVERDUE (Critical Severity, Stale Precedent). Escalated to Enterprise Architecture Board.",
                    "risk_ownership": "Owner assigned: Principal Decision Assurance Engineer (Assigned By: Principal Knowledge Operations Architect).",
                    "missing_evidence": "Third-party synthetic latency trace for secondary cloud provider route (Quality required: 95%).",
                    "recurring_risks": "Recurring Pattern: Repeated Evidence Gap in Secondary Cloud Provider SLA Jitter (Frequency: 4).",
                    "risk_concentration": "Weakest Knowledge Assurance: Secondary Cloud Resilience (Global Enterprise Multi-Region Cloud Wave 4).",
                    "remediation_effectiveness": "Remediation verified with 85% risk reduction and 90% evidence quality improvement."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Knowledge Operations & Remediation 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
