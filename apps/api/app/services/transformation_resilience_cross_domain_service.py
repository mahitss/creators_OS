import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_cross_domain_domains: Dict[str, dict] = {}
_in_memory_resilience_graphs: Dict[str, dict] = {}
_in_memory_graph_nodes: Dict[str, dict] = {}
_in_memory_graph_edges: Dict[str, dict] = {}
_in_memory_propagation_paths: Dict[str, dict] = {}
_in_memory_propagations: Dict[str, dict] = {}
_in_memory_systemic_exposures: Dict[str, dict] = {}
_in_memory_concentrations: Dict[str, dict] = {}
_in_memory_single_point_exposures: Dict[str, dict] = {}
_in_memory_fragilities: Dict[str, dict] = {}
_in_memory_redundancies: Dict[str, dict] = {}
_in_memory_resilience_gaps: Dict[str, dict] = {}
_in_memory_compound_risks: Dict[str, dict] = {}
_in_memory_compound_conditions: Dict[str, dict] = {}
_in_memory_cascade_projections: Dict[str, dict] = {}
_in_memory_cascade_breakpoints: Dict[str, dict] = {}
_in_memory_second_order_effects: Dict[str, dict] = {}
_in_memory_intervention_collisions: Dict[str, dict] = {}
_in_memory_governance_contexts: Dict[str, dict] = {}
_in_memory_systemic_warnings: Dict[str, dict] = {}

_EMITTED_CROSS_DOMAIN_EVENTS: List[dict] = []

EMITTED_CROSS_DOMAIN_EVENT_TYPES = [
    "transformation.resilience.cross_domain.domain.created",
    "transformation.resilience.cross_domain.node.projected",
    "transformation.resilience.cross_domain.edge.projected",
    "transformation.resilience.cross_domain.edge.validated",
    "transformation.resilience.cross_domain.propagation.detected",
    "transformation.resilience.cross_domain.systemic_exposure.detected",
    "transformation.resilience.cross_domain.concentration.detected",
    "transformation.resilience.cross_domain.single_point_exposure.detected",
    "transformation.resilience.cross_domain.fragility.detected",
    "transformation.resilience.cross_domain.redundancy.updated",
    "transformation.resilience.cross_domain.resilience_gap.detected",
    "transformation.resilience.cross_domain.compound_risk.detected",
    "transformation.resilience.cross_domain.cascade.detected",
    "transformation.resilience.cross_domain.cascade_breakpoint.detected",
    "transformation.resilience.cross_domain.scenario.created",
    "transformation.resilience.cross_domain.recommendation.created",
    "transformation.resilience.cross_domain.second_order_effect.detected",
    "transformation.resilience.cross_domain.intervention_collision.detected",
    "transformation.resilience.cross_domain.systemic_warning.created",
    "transformation.resilience.cross_domain.graph.rebuilt"
]

def _initialize_seed_cross_domain_data():
    if _in_memory_cross_domain_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Domain & Resilience Graph
    xdom1 = {
        "id": "xdom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Cross-Domain Resilience Intelligence Fabric 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Cross-Domain Resilience Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_cross_domain_domains[xdom1["id"]] = xdom1

    rgraph1 = {
        "id": "rgraph_01",
        "domain_id": xdom1["id"],
        "total_nodes_count": 12,
        "total_edges_count": 18,
        "status": "active",
        "updated_at": now_iso
    }
    _in_memory_resilience_graphs[rgraph1["id"]] = rgraph1

    # Graph Nodes (referencing existing entities without duplication)
    node_dep1 = {
        "id": "gnode_dep_01",
        "node_type": "dependency",
        "node_id": "dep_compute_cluster_01",
        "domain": "Infrastructure & Compute",
        "severity": "critical",
        "state": "active",
        "confidence": 0.98
    }
    _in_memory_graph_nodes[node_dep1["id"]] = node_dep1

    node_plan1 = {
        "id": "gnode_plan_01",
        "node_type": "plan",
        "node_id": "aplan_01",
        "domain": "Cloud Transformation Wave 3",
        "severity": "high",
        "state": "active",
        "confidence": 0.95
    }
    _in_memory_graph_nodes[node_plan1["id"]] = node_plan1

    node_plan2 = {
        "id": "gnode_plan_02",
        "node_type": "plan",
        "node_id": "aplan_hr_cloud_02",
        "domain": "HR Cloud Wave 4",
        "severity": "high",
        "state": "active",
        "confidence": 0.95
    }
    _in_memory_graph_nodes[node_plan2["id"]] = node_plan2

    node_risk1 = {
        "id": "gnode_risk_01",
        "node_type": "risk",
        "node_id": "emrisk_01",
        "domain": "Assurance Foresight",
        "severity": "high",
        "state": "active",
        "confidence": 0.95
    }
    _in_memory_graph_nodes[node_risk1["id"]] = node_risk1

    node_interv1 = {
        "id": "gnode_interv_01",
        "node_type": "intervention",
        "node_id": "icase_01",
        "domain": "Intervention Orchestration",
        "severity": "high",
        "state": "active",
        "confidence": 0.95
    }
    _in_memory_graph_nodes[node_interv1["id"]] = node_interv1

    # Graph Edges (with explicit relationship types)
    edge1 = {
        "id": "gedge_01",
        "source_node_id": node_plan1["id"],
        "target_node_id": node_dep1["id"],
        "relationship": "depends_on",
        "confidence": 0.98,
        "evidence_count": 3,
        "evidence_quality": 0.95,
        "last_validated_at": now_iso
    }
    _in_memory_graph_edges[edge1["id"]] = edge1

    edge2 = {
        "id": "gedge_02",
        "source_node_id": node_plan2["id"],
        "target_node_id": node_dep1["id"],
        "relationship": "depends_on",
        "confidence": 0.98,
        "evidence_count": 3,
        "evidence_quality": 0.95,
        "last_validated_at": now_iso
    }
    _in_memory_graph_edges[edge2["id"]] = edge2

    edge3 = {
        "id": "gedge_03",
        "source_node_id": node_risk1["id"],
        "target_node_id": node_dep1["id"],
        "relationship": "affects",
        "confidence": 0.95,
        "evidence_count": 2,
        "evidence_quality": 0.90,
        "last_validated_at": now_iso
    }
    _in_memory_graph_edges[edge3["id"]] = edge3

    # Propagation Path & Propagation
    ppath1 = {
        "id": "ppath_01",
        "source": "dep_compute_cluster_01",
        "target": "aplan_hr_cloud_02",
        "intermediate_nodes_json": ["gnode_plan_01", "gnode_risk_01"],
        "relationships_json": ["depends_on", "affects"],
        "depth": 3,
        "confidence": 0.95,
        "severity": "high"
    }
    _in_memory_propagation_paths[ppath1["id"]] = ppath1

    prop1 = {
        "id": "prop_01",
        "source_condition": "Gradual 15% compute cluster queue depth compression",
        "propagation_type": "dependency",
        "affected_objects_json": ["aplan_01", "aplan_hr_cloud_02", "icase_01"],
        "propagation_path_json": ["dep_compute_cluster_01 -> aplan_01 -> aplan_hr_cloud_02"],
        "estimated_impact": "Causes 7-day schedule shift across HR Cloud wave deployment.",
        "confidence": 0.95,
        "uncertainty": 0.08,
        "created_at": now_iso
    }
    _in_memory_propagations[prop1["id"]] = prop1

    # Systemic Exposure & Concentration
    sysexp1 = {
        "id": "sysexp_01",
        "title": "Systemic Compute Capacity & Wave Deployment Exposure",
        "affected_domains_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
        "affected_transformations_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
        "affected_plans_json": ["aplan_01", "aplan_hr_cloud_02"],
        "shared_dependencies_json": ["dep_compute_cluster_01"],
        "shared_resources_json": ["Simulation Cluster 01"],
        "severity": "critical",
        "exposure_state": "elevated",
        "confidence": 0.95,
        "uncertainty": 0.08
    }
    _in_memory_systemic_exposures[sysexp1["id"]] = sysexp1

    conc1 = {
        "id": "conc_01",
        "concentration_type": "dependency",
        "object_id": "dep_compute_cluster_01",
        "description": "85% of wave simulation compute load is concentrated on Cluster 01.",
        "concentration_score": 0.85,
        "created_at": now_iso
    }
    _in_memory_concentrations[conc1["id"]] = conc1

    # Single-Point Exposure, Fragility, Redundancy, Resilience Gap
    spexp1 = {
        "id": "spexp_01",
        "component_type": "shared dependency",
        "component_id": "dep_compute_cluster_01",
        "affected_systems_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4", "ERP Wave 5"],
        "severity": "high"
    }
    _in_memory_single_point_exposures[spexp1["id"]] = spexp1

    frag1 = {
        "id": "frag_01",
        "object_id": "dep_compute_cluster_01",
        "dependents_json": ["aplan_01", "aplan_hr_cloud_02"],
        "alternative_paths_count": 1,
        "recovery_options_json": ["Burst capacity node pool activation"],
        "confidence": 0.90,
        "created_at": now_iso
    }
    _in_memory_fragilities[frag1["id"]] = frag1

    red1 = {
        "id": "red_01",
        "object_id": "dep_compute_cluster_01",
        "alternative_evidence_json": ["Backup telemetry feed"],
        "alternative_dependencies_json": ["Secondary cloud compute cluster 02"],
        "alternative_resources_json": ["Reserved node pool"],
        "alternative_execution_paths_json": ["Preemptive resequencing batch"],
        "created_at": now_iso
    }
    _in_memory_redundancies[red1["id"]] = red1

    rgap1 = {
        "id": "rgap_01",
        "gap_type": "single_dependency",
        "description": "Lack of automated secondary cloud cluster failover for Wave 4 simulation runs.",
        "severity": "high",
        "recommended_mitigation": "Configure auto-scaling secondary cluster reserve."
    }
    _in_memory_resilience_gaps[rgap1["id"]] = rgap1

    # Compound Risk & Condition (with visible contributing factors)
    crisk1 = {
        "id": "crisk_01",
        "title": "Compound Compute Deficit & Governance Deadline Pressure Risk",
        "contributing_conditions_json": [
            "Moderate evidence staleness on queue depth (5%)",
            "Moderate deadline compression on Governance Board sign-off (5 days remaining)",
            "Shared compute cluster dependency concentration (85%)"
        ],
        "severity": "critical",
        "confidence": 0.92
    }
    _in_memory_compound_risks[crisk1["id"]] = crisk1

    ccond1 = {
        "id": "ccond_01",
        "compound_risk_id": crisk1["id"],
        "condition_description": "Shared dependency queue depth exceeds 85% threshold.",
        "relationship": "contributes_to",
        "threshold": 0.85,
        "confidence": 0.95,
        "evidence_ref": "evid_compute_01"
    }
    _in_memory_compound_conditions[ccond1["id"]] = ccond1

    # Cascade Projection & Breakpoint
    casc1 = {
        "id": "casc_01",
        "source_id": "dep_compute_cluster_01",
        "path_json": ["dep_compute_cluster_01", "aplan_01", "aplan_hr_cloud_02"],
        "affected_domains_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
        "depth": 3,
        "severity": "critical",
        "confidence": 0.90,
        "intervention_points_json": ["gnode_plan_01"]
    }
    _in_memory_cascade_projections[casc1["id"]] = casc1

    cbreak1 = {
        "id": "cbreak_01",
        "cascade_id": casc1["id"],
        "location_node_id": "gnode_plan_01",
        "option_type": "resequence",
        "expected_effect": "Staggers simulation runs by 7 days, eliminating 90% of downstream compute queue compression.",
        "confidence": 0.90,
        "cost": "low",
        "reversibility": "reversible",
        "created_at": now_iso
    }
    _in_memory_cascade_breakpoints[cbreak1["id"]] = cbreak1

    # Second-Order Effects & Intervention Collisions
    soeff1 = {
        "id": "soeff_01",
        "intervention_id": "icase_01",
        "affected_object_id": "aplan_hr_cloud_02",
        "effect_description": "Preemptive resequencing reduces compute bottleneck risk but shifts simulation batch into HR Cloud testing window.",
        "direction": "capacity_pressure_increased",
        "confidence": 0.90,
        "created_at": now_iso
    }
    _in_memory_second_order_effects[soeff1["id"]] = soeff1

    icoll1 = {
        "id": "icoll_01",
        "intervention_a_id": "icase_01",
        "intervention_b_id": "icase_hr_02",
        "collision_type": "compete",
        "affected_domains_json": ["HR Cloud Wave 4"],
        "resolution": "Stagger testing windows by 48 hours to eliminate capacity overlap.",
        "created_at": now_iso
    }
    _in_memory_intervention_collisions[icoll1["id"]] = icoll1

    # Governance Context & Systemic Warning
    gctx1 = {
        "id": "gctx_01",
        "required_authorities_json": ["Governance Board", "Cloud Infrastructure Lead"],
        "decision_dependencies_json": ["dpack_01"],
        "approval_dependencies_json": ["appr_01"],
        "policy_evaluation_ref": "peval_01"
    }
    _in_memory_governance_contexts[gctx1["id"]] = gctx1

    swarn1 = {
        "id": "swarn_01",
        "trigger_reason": "Systemic risk exposure detected: shared compute cluster dependency compression affecting Wave 3 and Wave 4.",
        "status": "open",
        "severity": "critical",
        "evidence_count": 4,
        "created_at": now_iso
    }
    _in_memory_systemic_warnings[swarn1["id"]] = swarn1

_initialize_seed_cross_domain_data()


class TransformationResilienceCrossDomainService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_CROSS_DOMAIN_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may analyze graph relationships, identify propagation, detect compound conditions, prepare systemic scenarios, identify cascade breakpoints, prepare recommendations.
        # Agents may NOT declare causal relationships without evidence, approve systemic decisions, execute interventions, or override governance.
        forbidden_actions = [
            "declare_causal_relationship_without_evidence", "approve_systemic_decisions",
            "execute_interventions", "override_governance"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing action '{action}'. Evidentiary causality and approval belong strictly to human governance."
            }
        return {"allowed": True, "reason": "Action permitted for cross-domain intelligence agent."}

    @staticmethod
    async def simulate_cross_domain_scenario(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_cross_domain_data()
        scen_id = f"xscen_{uuid.uuid4().hex[:8]}"
        scen = {
            "id": scen_id,
            "scenario_type": data.get("scenario_type", "single_dependency_failure"),
            "affected_objects_json": ["aplan_01", "aplan_hr_cloud_02"],
            "propagation_path_json": ["dep_compute_cluster_01 -> aplan_01 -> aplan_hr_cloud_02"],
            "risk_score": 0.88,
            "coverage_score": 0.90,
            "recovery_options_json": ["Activate secondary cloud compute cluster reserve"],
            "residual_exposure": 0.08,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        TransformationResilienceCrossDomainService.emit_event(
            "transformation.resilience.cross_domain.scenario.created", scen
        )
        return scen

    @staticmethod
    async def rebuild_graph(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_cross_domain_data()
        rgraph = list(_in_memory_resilience_graphs.values())[0]
        rgraph["status"] = "active"
        rgraph["updated_at"] = datetime.now(timezone.utc).isoformat()

        TransformationResilienceCrossDomainService.emit_event(
            "transformation.resilience.cross_domain.graph.rebuilt",
            {"status": "active", "timestamp": datetime.now(timezone.utc).isoformat()}
        )
        return {"status": "rebuilt", "graph_status": "active"}

    @staticmethod
    async def get_cross_domain_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_cross_domain_data()
        domains = list(_in_memory_cross_domain_domains.values())
        graphs = list(_in_memory_resilience_graphs.values())
        nodes = list(_in_memory_graph_nodes.values())
        edges = list(_in_memory_graph_edges.values())
        propagation_paths = list(_in_memory_propagation_paths.values())
        propagations = list(_in_memory_propagations.values())
        systemic_exposures = list(_in_memory_systemic_exposures.values())
        concentrations = list(_in_memory_concentrations.values())
        single_point_exposures = list(_in_memory_single_point_exposures.values())
        fragilities = list(_in_memory_fragilities.values())
        redundancies = list(_in_memory_redundancies.values())
        resilience_gaps = list(_in_memory_resilience_gaps.values())
        compound_risks = list(_in_memory_compound_risks.values())
        compound_conditions = list(_in_memory_compound_conditions.values())
        cascade_projections = list(_in_memory_cascade_projections.values())
        cascade_breakpoints = list(_in_memory_cascade_breakpoints.values())
        second_order_effects = list(_in_memory_second_order_effects.values())
        intervention_collisions = list(_in_memory_intervention_collisions.values())
        governance_contexts = list(_in_memory_governance_contexts.values())
        systemic_warnings = list(_in_memory_systemic_warnings.values())

        return {
            "domainsCount": len(domains),
            "nodesCount": len(nodes),
            "edgesCount": len(edges),
            "propagationsCount": len(propagations),
            "systemicExposuresCount": len(systemic_exposures),
            "compoundRisksCount": len(compound_risks),
            "cascadeProjectionsCount": len(cascade_projections),
            "cascadeBreakpointsCount": len(cascade_breakpoints),
            "secondOrderEffectsCount": len(second_order_effects),
            "interventionCollisionsCount": len(intervention_collisions),
            "systemicWarningsCount": len(systemic_warnings),
            "domains": domains,
            "resilienceGraphs": graphs,
            "nodes": nodes,
            "edges": edges,
            "propagationPaths": propagation_paths,
            "propagations": propagations,
            "systemicExposures": systemic_exposures,
            "concentrations": concentrations,
            "singlePointExposures": single_point_exposures,
            "fragilities": fragilities,
            "redundancies": redundancies,
            "resilienceGaps": resilience_gaps,
            "compoundRisks": compound_risks,
            "compoundConditions": compound_conditions,
            "cascadeProjections": cascade_projections,
            "cascadeBreakpoints": cascade_breakpoints,
            "secondOrderEffects": second_order_effects,
            "interventionCollisions": intervention_collisions,
            "governanceContexts": governance_contexts,
            "systemicWarnings": systemic_warnings
        }

    @staticmethod
    async def process_natural_language_cross_domain_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_cross_domain_data()

        # Anti-Surveillance / Privacy check (blocking employee-level systemic risk or employee behavioral fragility analysis)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee-level systemic risk", "employee behavioral fragility", "individual worker risk propagation",
            "rank worker fragility", "surveil employee risk"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee-level systemic risk scoring or employee behavioral fragility tracking."},
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
                    "connected_systems": "Shared Dependency 'dep_compute_cluster_01' (Simulation Compute Cluster 01) connects Cloud Transformation Wave 3 (aplan_01) and HR Cloud Wave 4 (aplan_hr_cloud_02).",
                    "single_point_exposures": "Single-Point Exposure 'spexp_01': Compute Cluster 01 supports 85% of wave simulation workload with zero secondary cluster redundancy.",
                    "propagation_path": "Propagation Path 'ppath_01' (Depth 3): dep_compute_cluster_01 -> aplan_01 -> aplan_hr_cloud_02 (Relationships: depends_on, affects).",
                    "compound_risks": "Compound Risk 'crisk_01' (Critical): Combining moderate evidence staleness (5%), deadline compression (5 days), and shared compute cluster dependency (85%).",
                    "cascade_breakpoints": "Cascade Breakpoint 'cbreak_01' at Node 'gnode_plan_01': Preemptive resequencing eliminates 90% of downstream compute queue compression.",
                    "second_order_effects": "Second-Order Effect 'soeff_01': Resequencing reduces compute bottleneck risk but increases capacity pressure during HR Cloud testing window.",
                    "intervention_collisions": "Intervention Collision 'icoll_01': Intervention icase_01 and icase_hr_02 compete for HR Cloud testing window capacity.",
                    "recommendation_notice": "ANALYTICAL RECOMMENDATION — NOT DECISION. Stagger simulation batch runs by 7 days to break systemic risk cascade."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Cross-Domain Assurance Intelligence Fabric 2.0",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.8
        }
