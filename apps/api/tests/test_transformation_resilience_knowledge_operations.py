import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_operations_service import TransformationResilienceKnowledgeOperationsService, _EMITTED_OPERATIONS_EVENTS

def test_get_knowledge_operations_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
        assert res["domainsCount"] >= 1
        assert res["casesCount"] >= 4
        assert res["criticalCount"] >= 1
        assert res["overdueCount"] >= 1
        assert res["plansCount"] >= 1
        assert res["evidenceTasksCount"] >= 1
        assert res["reviewTasksCount"] >= 1
        assert res["escalationsCount"] >= 1
        assert res["recurringPatternsCount"] >= 1
    asyncio.run(_test())

def test_risk_detection_triage_factor_breakdown_and_queues():
    async def _test():
        res = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
        rc = res["cases"][0]
        rq = res["queues"][0]
        assert rc["risk_type"] == "high_influence_low_quality"
        assert rc["severity"] == "high"
        assert rc["impact"] == "high_decision_impact"
        assert rq["status"] == "in_remediation"
    asyncio.run(_test())

def test_risk_owner_assignment_and_remediation_plan():
    async def _test():
        asgn = await TransformationResilienceKnowledgeOperationsService.assign_risk(
            None, "rcase_01", "Principal Decision Assurance Engineer", "Principal Knowledge Operations Architect", "High decision influence"
        )
        assert asgn["owner"] == "Principal Decision Assurance Engineer"
        assert asgn["assigned_by"] == "Principal Knowledge Operations Architect"
    asyncio.run(_test())

def test_evidence_task_non_fabrication_safety_and_review_tasks():
    async def _test():
        res = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
        et = res["evidenceTasks"][0]
        rt = res["reviewTasks"][0]
        assert et["requested_evidence"] == "Third-party synthetic latency trace for secondary cloud provider route"
        assert et["quality"] == 0.95
        assert rt["reviewer"] == "Principal Knowledge Governance Architect"
    asyncio.run(_test())

def test_remediation_verification_and_effectiveness_dimensions():
    async def _test():
        verif = await TransformationResilienceKnowledgeOperationsService.verify_remediation(None, "rcase_01", {
            "risk_before": {"severity": "high"},
            "risk_after": {"severity": "low"},
            "knowledge_health_before": {"freshness_score": 0.70},
            "knowledge_health_after": {"freshness_score": 0.96}
        })
        assert verif["risk_after"]["severity"] == "low"
        assert verif["knowledge_health_after"]["freshness_score"] == 0.96
    asyncio.run(_test())

def test_accepted_and_deferred_risks_and_overdue_sla():
    async def _test():
        res = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
        cases = res["cases"]
        accepted = [c for c in cases if c["status"] == "accepted_risk"][0]
        deferred = [c for c in cases if c["status"] == "deferred"][0]
        overdue = [c for c in cases if c["id"] == "rcase_overdue_01"][0]
        assert accepted["reason"] == "Legacy datacenter migration scheduled for Q4 will supersede this context."
        assert deferred["defer_until"] is not None
        assert overdue["status"] == "triaged"
    asyncio.run(_test())

def test_escalation_failures_recurring_patterns_and_concentration():
    async def _test():
        res = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
        esc = res["escalations"][0]
        fail = res["failures"][0]
        rec = res["recurring"][0]
        conc = res["riskConcentration"][0]
        assert esc["trigger"] == "sla_breached_critical_severity"
        assert fail["failure_category"] == "evidence_unavailable"
        assert rec["frequency"] == 4
        assert conc["domain"] == "Secondary Cloud Resilience"
    asyncio.run(_test())

def test_agent_governance_knowledge_operations_restrictions():
    # Agents may NOT approve remediation, accept risk, change governance, invalidate knowledge, or execute material changes
    chk_rem = TransformationResilienceKnowledgeOperationsService.enforce_agent_governance("agent_01", "approve_remediation")
    assert chk_rem["allowed"] is False
    assert "strictly blocked" in chk_rem["reason"]

    chk_acc = TransformationResilienceKnowledgeOperationsService.enforce_agent_governance("agent_01", "accept_risk")
    assert chk_acc["allowed"] is False

    chk_detect = TransformationResilienceKnowledgeOperationsService.enforce_agent_governance("agent_01", "detect_risks")
    assert chk_detect["allowed"] is True

def test_process_natural_language_operations_query_privacy_dlp_tenant():
    async def _test():
        # Valid operations query -> succeeds
        valid_q = "Which knowledge risks need attention and what remediation is underway?"
        res = await TransformationResilienceKnowledgeOperationsService.process_natural_language_operations_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee performance scores or remediation rankings) -> blocked
        surveil_q = "Rank employee remediation performance and generate employee behavioral profile"
        blocked_surveil = await TransformationResilienceKnowledgeOperationsService.process_natural_language_operations_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee performance scores" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show knowledge risk cases. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeOperationsService.process_natural_language_operations_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeOperationsService.process_natural_language_operations_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
