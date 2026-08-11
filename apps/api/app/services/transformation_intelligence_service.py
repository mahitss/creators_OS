import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_nodes: Dict[str, dict] = {}
_in_memory_edges: Dict[str, dict] = {}
_in_memory_provenances: Dict[str, dict] = {}
_in_memory_impact_maps: Dict[str, dict] = {}
_in_memory_cross_impacts: Dict[str, dict] = {}
_in_memory_capability_overlaps: Dict[str, dict] = {}
_in_memory_assumption_clusters: Dict[str, dict] = {}
_in_memory_scenario_exposures: Dict[str, dict] = {}
_in_memory_benefit_graphs: Dict[str, dict] = {}
_in_memory_conflict_graphs: Dict[str, dict] = {}
_in_memory_decision_props: Dict[str, dict] = {}
_in_memory_risk_props: Dict[str, dict] = {}
_in_memory_lesson_props: Dict[str, dict] = {}
_in_memory_patterns: Dict[str, dict] = {}
_in_memory_analogies: Dict[str, dict] = {}
_in_memory_complexity_profiles: Dict[str, dict] = {}
_in_memory_complexity_hotspots: Dict[str, dict] = {}
_in_memory_knowledge_conflicts: Dict[str, dict] = {}
_in_memory_graph_snapshots: Dict[str, dict] = {}
_in_memory_graph_diffs: Dict[str, dict] = {}
_in_memory_bottleneck_clusters: Dict[str, dict] = {}

def _initialize_seed_transformation_intelligence_data():
    if _in_memory_nodes:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"

    # Seed Nodes
    n1 = {
        "id": "node_cand_01",
        "organization_id": org_id,
        "entity_type": "transformation",
        "entity_id": "cand_01",
        "label": "Skill Certification Auto-signer Transformation",
        "status": "active",
        "source": "Transformation Portfolio Service",
        "confidence": 0.98,
        "freshness": "realtime",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    n2 = {
        "id": "node_cand_02",
        "organization_id": org_id,
        "entity_type": "transformation",
        "entity_id": "cand_02",
        "label": "Autonomous FinOps Scale Transformation",
        "status": "active",
        "source": "Transformation Portfolio Service",
        "confidence": 0.96,
        "freshness": "realtime",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    n3 = {
        "id": "node_cap_compliance",
        "organization_id": org_id,
        "entity_type": "capability",
        "entity_id": "cap_zero_trust_compliance",
        "label": "Zero-Trust Compliance Engine Capability",
        "status": "active",
        "source": "Capability Registry",
        "confidence": 0.99,
        "freshness": "realtime",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_nodes[n1["id"]] = n1
    _in_memory_nodes[n2["id"]] = n2
    _in_memory_nodes[n3["id"]] = n3

    # Seed Edges & Provenance
    e1 = {
        "id": "edge_dep_cand01_cand02",
        "organization_id": org_id,
        "from_node_id": n2["id"],
        "to_node_id": n1["id"],
        "relationship_type": "depends_on",
        "strength": 0.95,
        "confidence": 0.98,
        "source": "Transformation Dependency Graph Engine",
        "observed_at": now_iso,
        "expires_at": None
    }
    e2 = {
        "id": "edge_enables_cap_cand01",
        "organization_id": org_id,
        "from_node_id": n1["id"],
        "to_node_id": n3["id"],
        "relationship_type": "enables",
        "strength": 0.90,
        "confidence": 0.94,
        "source": "Operating Model Engine",
        "observed_at": now_iso,
        "expires_at": None
    }
    _in_memory_edges[e1["id"]] = e1
    _in_memory_edges[e2["id"]] = e2

    prov1 = {
        "id": "prov_01",
        "edge_id": e1["id"],
        "source_system": "Dependency Matrix Analysis",
        "method": "AST Schema Parsing",
        "evidence_json": {"pre_signer_token_dependency": "FinOps scaling requires Zero-Trust pre-signing API"},
        "confidence": 0.98,
        "classified_as": "observed"
    }
    _in_memory_provenances[prov1["id"]] = prov1

    # Seed Cross-Transformation Impact & Capability Overlap
    cross1 = {
        "id": "cross_01",
        "source_transformation_id": "cand_01",
        "target_transformation_id": "cand_02",
        "impact_type": "enabling",
        "severity": "high",
        "confidence": 0.95,
        "evidence_json": {"enabling_effect": "Unlocks sub-100ms policy authorization for FinOps execution"}
    }
    _in_memory_cross_impacts[cross1["id"]] = cross1

    cap_ov1 = {
        "id": "capov_01",
        "capability_id": "cap_zero_trust_compliance",
        "transformation_ids_json": ["cand_01", "cand_02"],
        "capacity_demand_json": {"engineering": "45%", "compliance": "25%"},
        "risk_score": 0.12,
        "conflict_flag": False
    }
    _in_memory_capability_overlaps[cap_ov1["id"]] = cap_ov1

    # Seed Assumption Cluster & Scenario Exposure
    ass1 = {
        "id": "ass_01",
        "shared_assumption": "Open API AST rule schema stability across enterprise mesh",
        "transformation_ids_json": ["cand_01", "cand_02"],
        "exposure_level": "medium",
        "confidence": 0.92
    }
    _in_memory_assumption_clusters[ass1["id"]] = ass1

    scen1 = {
        "id": "scen_exp_01",
        "scenario_id": "scen_rapid_api_volume_surge",
        "transformation_ids_json": ["cand_01", "cand_02"],
        "vulnerability_score": 0.08,
        "impact_desc": "Low vulnerability; pre-signer caching absorbs up to 10x API volume surge"
    }
    _in_memory_scenario_exposures[scen1["id"]] = scen1

    # Seed Benefit Graph & Conflict Graph
    bg1 = {
        "id": "bgraph_01",
        "transformation_ids_json": ["cand_01", "cand_02"],
        "claimed_benefit": "Aggregate 30% reduction in cloud infrastructure operational expenditure",
        "overlap_flag": False,
        "outcome_connection": "Enterprise Autonomous FinOps & Scalable Compliance"
    }
    _in_memory_benefit_graphs[bg1["id"]] = bg1

    cg1 = {
        "id": "cgraph_01",
        "transformation_a_id": "cand_01",
        "transformation_b_id": "cand_02",
        "conflict_domain": "capacity",
        "severity": "low",
        "evidence_json": {"capacity_friction": "Transient Q3 engineering overlap during initial wave rollout"}
    }
    _in_memory_conflict_graphs[cg1["id"]] = cg1

    # Seed Pattern, Analogy, & Hotspot
    pat1 = {
        "id": "pat_01",
        "pattern_name": "Foundational Pre-signer Unlocks Downstream Automation",
        "pattern_type": "enabling_sequence",
        "supporting_evidence_json": {"historical_velocity_boost": "2.4x acceleration in post-foundation waves"},
        "confidence": 0.95
    }
    _in_memory_patterns[pat1["id"]] = pat1

    an1 = {
        "id": "analogy_01",
        "current_transformation_id": "cand_01",
        "historical_transformation_id": "transprog_policy_v1",
        "similarity_score": 0.88,
        "key_differences_json": ["V2 uses zero-trust AST pre-signing instead of legacy sync RPC"],
        "confidence": 0.91
    }
    _in_memory_analogies[an1["id"]] = an1

    hs1 = {
        "id": "hotspot_01",
        "hotspot_name": "Zero-Trust Compliance Capability Convergence",
        "converging_transformation_ids_json": ["cand_01", "cand_02"],
        "hotspot_domain": "capability",
        "severity": "medium"
    }
    _in_memory_complexity_hotspots[hs1["id"]] = hs1

    # Seed Snapshot & Diff
    snap1 = {
        "id": "snap_01",
        "organization_id": org_id,
        "snapshot_label": "Q3 2026 Baseline Transformation Knowledge Graph",
        "nodes_count": len(_in_memory_nodes),
        "edges_count": len(_in_memory_edges),
        "created_at": now_iso
    }
    _in_memory_graph_snapshots[snap1["id"]] = snap1

_initialize_seed_transformation_intelligence_data()


class TransformationIntelligenceService:

    @staticmethod
    async def get_fabric_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_transformation_intelligence_data()
        nodes = list(_in_memory_nodes.values())
        edges = list(_in_memory_edges.values())
        provenances = list(_in_memory_provenances.values())
        cross_impacts = list(_in_memory_cross_impacts.values())
        capability_overlaps = list(_in_memory_capability_overlaps.values())
        assumption_clusters = list(_in_memory_assumption_clusters.values())
        scenario_exposures = list(_in_memory_scenario_exposures.values())
        benefit_graphs = list(_in_memory_benefit_graphs.values())
        conflict_graphs = list(_in_memory_conflict_graphs.values())
        patterns = list(_in_memory_patterns.values())
        analogies = list(_in_memory_analogies.values())
        hotspots = list(_in_memory_complexity_hotspots.values())
        snapshots = list(_in_memory_graph_snapshots.values())

        return {
            "graphNodesCount": len(nodes),
            "graphEdgesCount": len(edges),
            "provenanceRecordsCount": len(provenances),
            "crossTransformationImpactsCount": len(cross_impacts),
            "capabilityOverlapsCount": len(capability_overlaps),
            "sharedAssumptionClustersCount": len(assumption_clusters),
            "scenarioExposuresCount": len(scenario_exposures),
            "benefitGraphsCount": len(benefit_graphs),
            "conflictGraphsCount": len(conflict_graphs),
            "patternsDetectedCount": len(patterns),
            "analogiesIdentifiedCount": len(analogies),
            "complexityHotspotsCount": len(hotspots),
            "graphSnapshotsCount": len(snapshots),
            "overallFabricDensityScore": 0.88,
            "nodes": nodes,
            "edges": edges,
            "provenances": provenances,
            "crossImpacts": cross_impacts,
            "capabilityOverlaps": capability_overlaps,
            "assumptionClusters": assumption_clusters,
            "scenarioExposures": scenario_exposures,
            "benefitGraphs": benefit_graphs,
            "conflictGraphs": conflict_graphs,
            "patterns": patterns,
            "analogies": analogies,
            "hotspots": hotspots,
            "snapshots": snapshots
        }

    @staticmethod
    async def query_multi_hop_paths(session: Optional[AsyncSession], from_entity: str, to_entity: str) -> dict:
        _initialize_seed_transformation_intelligence_data()

        path_nodes = [
            {"step": 1, "entity_type": "transformation", "id": "cand_01", "label": "Skill Certification Auto-signer Transformation"},
            {"step": 2, "entity_type": "capability", "id": "cap_zero_trust_compliance", "label": "Zero-Trust Compliance Engine Capability"},
            {"step": 3, "entity_type": "transformation", "id": "cand_02", "label": "Autonomous FinOps Scale Transformation"}
        ]

        edges = [
            {"from": "cand_01", "to": "cap_zero_trust_compliance", "relationship": "enables", "provenance": "observed"},
            {"from": "cand_02", "to": "cand_01", "relationship": "depends_on", "provenance": "observed"}
        ]

        return {
            "fromEntity": from_entity,
            "toEntity": to_entity,
            "multiHopPath": path_nodes,
            "relationships": edges,
            "confidencePct": 96.0,
            "evidence": "Observed dependency matrix + capability enablement graph."
        }

    @staticmethod
    async def process_natural_language_intelligence_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_transformation_intelligence_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking employee relationship graphs / individual worker tracking)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee graph", "worker relationship", "surveil employee", "individual worker graph", "rank employee"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee relationship graphs, worker surveillance, individual productivity tracking, or employment penalty recommendations."},
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

        return {
            "query": query_str,
            "results": [
                {
                    "primary_root_dependency": "Skill Certification Auto-signer Transformation (cand_01)",
                    "shared_capability_overlap": "Zero-Trust Compliance Engine Capability (Shared by cand_01 and cand_02)",
                    "cross_transformation_impact": "cand_01 enables sub-100ms policy authorization for cand_02",
                    "shared_assumption_cluster": "Open API AST rule schema stability across enterprise mesh",
                    "benefit_graph_finding": "Aggregate 30% cost reduction claims are non-overlapping & verified",
                    "complexity_hotspot": "Zero-Trust Compliance Capability Convergence (Severity: medium)",
                    "historical_analogy": "88% similarity to Policy Engine V1 transformation"
                }
            ],
            "evidenceJson": {
                "data_source": "Cross-Transformation Knowledge Graph 2.0 Engine",
                "edges_evaluated": len(_in_memory_edges)
            },
            "confidencePct": 97.0
        }
