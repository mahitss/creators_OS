import pytest
import asyncio
from app.services.transformation_resilience_assurance_command_service import TransformationResilienceAssuranceCommandService

def test_event_projection():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.project_event(None, {
            "id": "evt_test_01",
            "event_type": "transformation.resilience.assurance.command.event.projected",
            "source_domain": "Foresight",
            "severity": "high"
        })
        assert res["status"] == "projected"
        assert res["event_id"] == "evt_test_01"
    asyncio.run(_test())

def test_event_duplication():
    async def _test():
        # First send
        res1 = await TransformationResilienceAssuranceCommandService.project_event(None, {
            "id": "evt_dup_01",
            "event_type": "transformation.resilience.assurance.command.event.projected",
            "severity": "high"
        })
        assert res1["status"] == "projected"

        # Duplicate send
        res2 = await TransformationResilienceAssuranceCommandService.project_event(None, {
            "id": "evt_dup_01",
            "event_type": "transformation.resilience.assurance.command.event.projected",
            "severity": "high"
        })
        assert res2["status"] == "ignored_duplicate"
    asyncio.run(_test())

def test_out_of_order_event():
    async def _test():
        # Out of order event projection must process gracefully
        res = await TransformationResilienceAssuranceCommandService.project_event(None, {
            "id": "evt_ooo_01",
            "event_type": "transformation.resilience.assurance.command.event.projected",
            "severity": "critical",
            "timestamp": "2026-08-14T10:00:00Z"
        })
        assert res["status"] == "projected"
    asyncio.run(_test())

def test_snapshot():
    async def _test():
        snap = await TransformationResilienceAssuranceCommandService.create_command_snapshot(None, "Test Snapshot")
        assert snap["label"] == "Test Snapshot"
        assert "state_data_json" in snap
    asyncio.run(_test())

def test_snapshot_diff():
    async def _test():
        diff = await TransformationResilienceAssuranceCommandService.diff_command_snapshots(None, "csnap_01", "csnap_02")
        assert diff["previous_snapshot_id"] == "csnap_01"
        assert diff["current_snapshot_id"] == "csnap_02"
        assert "emrisk_02" in diff["new_risks_json"]
    asyncio.run(_test())

def test_decision_bottleneck():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        dbott = res["decisionBottlenecks"][0]
        abott = res["approvalBottlenecks"][0]
        assert dbott["bottleneck_type"] == "approval_delay"
        assert abott["required_authority"] == "Governance Board"
    asyncio.run(_test())

def test_dependency_hotspot():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        dhot = res["dependencyHotspots"][0]
        assert dhot["name"] == "Simulation Compute Cluster 01"
        assert dhot["affected_plans_count"] == 5
    asyncio.run(_test())

def test_resource_pressure():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        rpress = res["resourcePressures"][0]
        assert rpress["resource_category"] == "compute_capacity"
        assert rpress["pressure_level"] == "elevated"
        # Must not contain individual employee rankings
        assert "employee" not in str(rpress).lower()
    asyncio.run(_test())

def test_knowledge_health():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        kh = res["knowledgeHealthProjections"][0]
        assert kh["evidence_freshness"] == 0.95
        assert kh["coverage"] == 0.92
    asyncio.run(_test())

def test_transformation_health():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        th = res["transformationHealthProjections"][0]
        assert th["transformation_name"] == "Cloud Transformation Wave 3"
        assert th["residual_exposure"] == 0.08
    asyncio.run(_test())

def test_scene():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        sc = res["operationalScenes"][0]
        assert sc["status"] == "active"
        assert "Compute Load Compression" in sc["title"]
    asyncio.run(_test())

def test_scene_relationship():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        srel = res["sceneRelationships"][0]
        assert srel["relationship_type"] in ["causes", "contributes_to", "depends_on", "blocks", "mitigates", "follows", "correlates_with", "unknown"]
    asyncio.run(_test())

def test_escalation():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        esc = res["escalations"][0]
        assert esc["status"] == "detected"
        assert "deadline breach" in esc["trigger_reason"]
    asyncio.run(_test())

def test_degraded_mode():
    async def _test():
        res = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
        phealth = res["projectionHealths"][0]
        assert phealth["rebuild_status"] == "idle"
        assert phealth["lag_seconds"] == 0.12
    asyncio.run(_test())

def test_rebuild():
    async def _test():
        reb_res = await TransformationResilienceAssuranceCommandService.rebuild_projections(None)
        assert reb_res["status"] == "rebuilt"
        assert reb_res["rebuild_status"] == "completed"
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceAssuranceCommandService.enforce_agent_governance("agent_command_01", "summarize_operational_state")
    assert res1["allowed"] is True

    res2 = TransformationResilienceAssuranceCommandService.enforce_agent_governance("agent_command_01", "declare_enterprise_status")
    assert res2["allowed"] is False

    res3 = TransformationResilienceAssuranceCommandService.enforce_agent_governance("agent_command_01", "approve_decisions")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy blocked query
        p_res = await TransformationResilienceAssuranceCommandService.process_natural_language_assurance_command_query(
            None, "Surveil worker productivity and rank employee utilization"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP blocked query
        dlp_res = await TransformationResilienceAssuranceCommandService.process_natural_language_assurance_command_query(
            None, "Show command status for secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceAssuranceCommandService.process_natural_language_assurance_command_query(
            None, "What is happening right now?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())
