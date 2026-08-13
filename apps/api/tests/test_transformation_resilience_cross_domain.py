import pytest
import asyncio
from app.services.transformation_resilience_cross_domain_service import TransformationResilienceCrossDomainService

def test_graph():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        nodes = res["nodes"]
        edges = res["edges"]
        dep_node = [n for n in nodes if n["node_type"] == "dependency"][0]
        dep_edges = [e for e in edges if e["target_node_id"] == dep_node["id"] or e["target_node_id"] == dep_node["node_id"]]
        assert dep_node["node_id"] == "dep_compute_cluster_01"
        assert len(dep_edges) >= 2
    asyncio.run(_test())

def test_propagation():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        prop = res["propagations"][0]
        assert prop["propagation_type"] == "dependency"
        assert len(prop["affected_objects_json"]) >= 2
        assert prop["confidence"] == 0.95
    asyncio.run(_test())

def test_systemic_exposure():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        sysexp = res["systemicExposures"][0]
        assert sysexp["severity"] == "critical"
        assert "dep_compute_cluster_01" in sysexp["shared_dependencies_json"]
    asyncio.run(_test())

def test_single_point():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        sp = res["singlePointExposures"][0]
        assert sp["component_type"] == "shared dependency"
        assert sp["component_id"] == "dep_compute_cluster_01"
    asyncio.run(_test())

def test_redundancy():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        red = res["redundancies"][0]
        assert red["object_id"] == "dep_compute_cluster_01"
    asyncio.run(_test())

def test_fragility():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        frag = res["fragilities"][0]
        assert frag["object_id"] == "dep_compute_cluster_01"
        assert len(frag["dependents_json"]) >= 2
    asyncio.run(_test())

def test_compound_risk():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        crisk = res["compoundRisks"][0]
        assert crisk["severity"] == "critical"
        # Contributing conditions MUST remain explicitly visible
        assert len(crisk["contributing_conditions_json"]) >= 3
    asyncio.run(_test())

def test_causality():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        edges = res["edges"]
        # All edges must use supported explicit relationship types
        allowed_rels = ["depends_on", "supports", "blocks", "affects", "shared_with", "constrained_by", "derived_from", "mitigates", "causes", "contributes_to", "correlates_with", "precedes", "governed_by"]
        for e in edges:
            assert e["relationship"] in allowed_rels
    asyncio.run(_test())

def test_cascade():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        casc = res["cascadeProjections"][0]
        assert casc["depth"] == 3
        assert casc["severity"] == "critical"
    asyncio.run(_test())

def test_breakpoint():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        cb = res["cascadeBreakpoints"][0]
        assert cb["option_type"] == "resequence"
        assert cb["reversibility"] == "reversible"
    asyncio.run(_test())

def test_second_order():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        so = res["secondOrderEffects"][0]
        assert so["direction"] in ["risk_reduced", "capacity_pressure_increased", "deadline_improved", "new_dependency_created"]
        assert "testing window" in so["effect_description"].lower() or "capacity" in so["effect_description"].lower()
    asyncio.run(_test())


def test_intervention_collision():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        icoll = res["interventionCollisions"][0]
        assert icoll["collision_type"] == "compete"
        assert "Stagger testing windows" in icoll["resolution"]
    asyncio.run(_test())

def test_systemic_warning():
    async def _test():
        res = await TransformationResilienceCrossDomainService.get_cross_domain_overview(None)
        swarn = res["systemicWarnings"][0]
        assert swarn["status"] == "open"
        assert swarn["severity"] == "critical"
    asyncio.run(_test())

def test_scenario():
    async def _test():
        scen = await TransformationResilienceCrossDomainService.simulate_cross_domain_scenario(None, {"scenario_type": "single_dependency_failure"})
        assert scen["scenario_type"] == "single_dependency_failure"
        assert scen["risk_score"] == 0.88
    asyncio.run(_test())

def test_graph_rebuild():
    async def _test():
        reb_res = await TransformationResilienceCrossDomainService.rebuild_graph(None)
        assert reb_res["status"] == "rebuilt"
        assert reb_res["graph_status"] == "active"
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceCrossDomainService.enforce_agent_governance("agent_cross_01", "analyze_graph_relationships")
    assert res1["allowed"] is True

    res2 = TransformationResilienceCrossDomainService.enforce_agent_governance("agent_cross_01", "declare_causal_relationship_without_evidence")
    assert res2["allowed"] is False

    res3 = TransformationResilienceCrossDomainService.enforce_agent_governance("agent_cross_01", "approve_systemic_decisions")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy blocked query
        p_res = await TransformationResilienceCrossDomainService.process_natural_language_cross_domain_query(
            None, "Analyze employee-level systemic risk and rank employee behavioral fragility"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP blocked query
        dlp_res = await TransformationResilienceCrossDomainService.process_natural_language_cross_domain_query(
            None, "Show propagation path for secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceCrossDomainService.process_natural_language_cross_domain_query(
            None, "Which risks compound across Wave 3 and Wave 4?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())
