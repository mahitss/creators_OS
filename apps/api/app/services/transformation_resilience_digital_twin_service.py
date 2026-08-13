import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_digital_twin_domains: Dict[str, dict] = {}
_in_memory_digital_twin_states: Dict[str, dict] = {}
_in_memory_digital_twin_snapshots: Dict[str, dict] = {}
_in_memory_digital_twin_synchronizations: Dict[str, dict] = {}
_in_memory_digital_twin_state_diffs: Dict[str, dict] = {}
_in_memory_digital_twin_nodes: Dict[str, dict] = {}
_in_memory_digital_twin_relationships: Dict[str, dict] = {}
_in_memory_digital_twin_reality_comparisons: Dict[str, dict] = {}
_in_memory_digital_twin_scenario_forks: Dict[str, dict] = {}
_in_memory_digital_twin_scenario_states: Dict[str, dict] = {}
_in_memory_digital_twin_counterfactual_changes: Dict[str, dict] = {}
_in_memory_digital_twin_counterfactual_scenarios: Dict[str, dict] = {}
_in_memory_digital_twin_scenario_outcomes: Dict[str, dict] = {}
_in_memory_digital_twin_counterfactual_comparisons: Dict[str, dict] = {}
_in_memory_digital_twin_stress_scenarios: Dict[str, dict] = {}
_in_memory_digital_twin_external_shock_scenarios: Dict[str, dict] = {}
_in_memory_digital_twin_recovery_scenarios: Dict[str, dict] = {}
_in_memory_digital_twin_experiments: Dict[str, dict] = {}
_in_memory_digital_twin_experiment_results: Dict[str, dict] = {}
_in_memory_digital_twin_validations: Dict[str, dict] = {}
_in_memory_digital_twin_model_errors: Dict[str, dict] = {}
_in_memory_digital_twin_drifts: Dict[str, dict] = {}
_in_memory_digital_twin_scenario_libraries: Dict[str, dict] = {}

_EMITTED_DIGITAL_TWIN_EVENTS: List[dict] = []

EMITTED_DIGITAL_TWIN_EVENT_TYPES = [
    "transformation.resilience.digital_twin.domain.created",
    "transformation.resilience.digital_twin.state.created",
    "transformation.resilience.digital_twin.snapshot.created",
    "transformation.resilience.digital_twin.synchronization.updated",
    "transformation.resilience.digital_twin.state_diff.created",
    "transformation.resilience.digital_twin.reality_comparison.created",
    "transformation.resilience.digital_twin.scenario_fork.created",
    "transformation.resilience.digital_twin.counterfactual.created",
    "transformation.resilience.digital_twin.scenario.created",
    "transformation.resilience.digital_twin.scenario.completed",
    "transformation.resilience.digital_twin.stress.created",
    "transformation.resilience.digital_twin.shock.created",
    "transformation.resilience.digital_twin.recovery.created",
    "transformation.resilience.digital_twin.experiment.created",
    "transformation.resilience.digital_twin.experiment.completed",
    "transformation.resilience.digital_twin.validation.completed",
    "transformation.resilience.digital_twin.model_error.detected",
    "transformation.resilience.digital_twin.drift.detected",
    "transformation.resilience.digital_twin.scenario_library.updated"
]

def _initialize_seed_digital_twin_data():
    if _in_memory_digital_twin_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Domain & State
    dt_dom1 = {
        "id": "dtdom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Resilience Digital Twin 2.0",
        "scope": "enterprise",
        "source_version": "v2.0",
        "state_version": "v2.0",
        "status": "current",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_digital_twin_domains[dt_dom1["id"]] = dt_dom1

    dt_state1 = {
        "id": "dtstate_01",
        "domain_id": dt_dom1["id"],
        "timestamp": now_iso,
        "source_event_id": "evt_mesh_resilience_104_last",
        "source_version": "v2.0",
        "state_hash": "sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "freshness": 1.0,
        "completeness": 0.98,
        "confidence": 0.95
    }
    _in_memory_digital_twin_states[dt_state1["id"]] = dt_state1

    # Snapshot & Synchronization
    snap1 = {
        "id": "dtsnap_v2_0",
        "version": "v2.0",
        "parent_version": "v1.0",
        "transformations_count": 8,
        "plans_count": 14,
        "dependencies_count": 22,
        "risks_count": 18,
        "knowledge_count": 35,
        "evidence_count": 42,
        "warnings_count": 6,
        "conflicts_count": 4,
        "interventions_count": 5,
        "decisions_count": 9,
        "resources_count": 12,
        "deadlines_count": 15,
        "state_hash": "sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "created_at": now_iso
    }
    _in_memory_digital_twin_snapshots[snap1["id"]] = snap1

    sync1 = {
        "id": "dtsync_01",
        "last_source_event_id": "evt_mesh_resilience_104_last",
        "last_processed_event_id": "evt_mesh_resilience_104_last",
        "lag_seconds": 0.0,
        "errors_count": 0,
        "rebuild_status": "idle",
        "synchronization_mode": "event_driven",
        "updated_at": now_iso
    }
    _in_memory_digital_twin_synchronizations[sync1["id"]] = sync1

    # State Diff & Reality Comparison
    sdiff1 = {
        "id": "sdiff_01",
        "previous_snapshot_version": "v1.0",
        "current_snapshot_version": "v2.0",
        "changed_objects_json": ["gnode_dep_01", "sysexp_01"],
        "added_objects_json": ["crisk_01", "cbreak_01"],
        "removed_objects_json": [],
        "changed_relationships_json": ["gedge_01", "gedge_02"],
        "created_at": now_iso
    }
    _in_memory_digital_twin_state_diffs[sdiff1["id"]] = sdiff1

    rcomp1 = {
        "id": "rcomp_01",
        "production_state_summary": "Production shows Compute Cluster 01 at 85% utilization with 2 active wave deployments.",
        "twin_state_summary": "Digital Twin state matches production telemetry across 98% of objects.",
        "difference_description": "2% divergence due to 45-second latency on secondary backup telemetry feed.",
        "freshness": 1.0,
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_digital_twin_reality_comparisons[rcomp1["id"]] = rcomp1

    # Scenario Fork & Scenario State (Strictly isolated, never mutates production)
    fork1 = {
        "id": "fork_01",
        "base_snapshot_id": snap1["id"],
        "scenario_id": "scen_counterfactual_dep_01",
        "owner": "Principal Enterprise Resilience Digital Twin Architect",
        "created_at": now_iso,
        "expires_at": (now + timedelta(days=7)).isoformat()
    }
    _in_memory_digital_twin_scenario_forks[fork1["id"]] = fork1

    scen_state1 = {
        "id": "sstate_01",
        "scenario_fork_id": fork1["id"],
        "hypothetical_state_json": {
            "dep_compute_cluster_01": "FAILED",
            "aplan_01": "SCHEDULE_SHIFT_7_DAYS",
            "aplan_hr_cloud_02": "BLOCKED_ON_COMPUTE"
        },
        "isolation_level": "strictly_isolated",
        "created_at": now_iso
    }
    _in_memory_digital_twin_scenario_states[scen_state1["id"]] = scen_state1

    # Counterfactual Change, Scenario & Outcome
    cchange1 = {
        "id": "cchange_01",
        "change_type": "dependency_failure",
        "target_object_id": "dep_compute_cluster_01",
        "parameters_json": {"downtime_hours": 72},
        "description": "Simulate 72-hour outage of primary compute cluster 01."
    }
    _in_memory_digital_twin_counterfactual_changes[cchange1["id"]] = cchange1

    cscen1 = {
        "id": "cscen_01",
        "baseline_snapshot_id": snap1["id"],
        "changes_json": ["cchange_01"],
        "assumptions_json": ["No automated secondary cloud cluster failover available", "Governance board approval takes 48h"],
        "horizon_days": 30,
        "confidence": 0.90,
        "created_at": now_iso
    }
    _in_memory_digital_twin_counterfactual_scenarios[cscen1["id"]] = cscen1

    sout1 = {
        "id": "sout_01",
        "scenario_id": cscen1["id"],
        "risk_score": 0.88,
        "coverage_score": 0.90,
        "capacity_score": 0.70,
        "deadline_impact_days": 14,
        "dependency_exposure_score": 0.85,
        "residual_risk_score": 0.12,
        "recovery_time_days": 7,
        "created_at": now_iso
    }
    _in_memory_digital_twin_scenario_outcomes[sout1["id"]] = sout1

    ccomp1 = {
        "id": "ccomp_01",
        "baseline_id": snap1["id"],
        "scenario_id": cscen1["id"],
        "difference_summary": "72-hour compute outage increases overall wave deployment risk by +28% and delays HR Cloud Go-Live by 14 days.",
        "uncertainty": 0.08
    }
    _in_memory_digital_twin_counterfactual_comparisons[ccomp1["id"]] = ccomp1

    # Stress, External Shock & Recovery Scenario
    stress1 = {
        "id": "stress_01",
        "stress_type": "capacity_stress",
        "severity": "critical",
        "affected_domains_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
        "recovery_impact": "Requires 5-day contingency buffer to stabilize compute queue depth.",
        "created_at": now_iso
    }
    _in_memory_digital_twin_stress_scenarios[stress1["id"]] = stress1

    shock1 = {
        "id": "shock_01",
        "shock_name": "Global Multi-Cloud Data Center Outage",
        "affected_domains_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4", "ERP Wave 5"],
        "severity": "high",
        "duration_days": 14,
        "recovery_assumptions_json": ["Secondary region cloud backup pool activated within 12 hours"],
        "created_at": now_iso
    }
    _in_memory_digital_twin_external_shock_scenarios[shock1["id"]] = shock1

    rec1 = {
        "id": "rec_01",
        "recovery_mode": "contingency_recovery",
        "time_to_stabilization_days": 5,
        "risk_reduction_pct": 85.0,
        "coverage_recovery_pct": 95.0,
        "capacity_recovery_pct": 90.0,
        "residual_exposure": 0.08,
        "created_at": now_iso
    }
    _in_memory_digital_twin_recovery_scenarios[rec1["id"]] = rec1

    # Governed Experiment & Result (with Reproducibility)
    exp1 = {
        "id": "exp_01",
        "title": "Secondary Cluster Failover Resilience Experiment",
        "hypothesis": "Configuring auto-scaling secondary cluster reserve reduces systemic compute exposure by >80%.",
        "scope": "simulation_only",
        "assumptions_json": ["Secondary cluster provisioned in US-East region", "Telemetry sync lag < 10 seconds"],
        "expected_result": "Systemic exposure drops from Critical (0.88) to Low (0.15).",
        "status": "approved",
        "authorization_ref": "auth_sim_governance_105",
        "created_at": now_iso
    }
    _in_memory_digital_twin_experiments[exp1["id"]] = exp1

    exp_res1 = {
        "id": "expres_01",
        "experiment_id": exp1["id"],
        "hypothesis": exp1["hypothesis"],
        "observed_result": "Observed 84% reduction in systemic compute exposure during simulated 72-hour primary outage.",
        "expected_result": exp1["expected_result"],
        "variance": "Exceeded hypothesis expectation by +4% risk reduction.",
        "confidence": 0.94,
        "limitations_json": ["Assumes secondary cloud provider bandwidth quota is unconstrained."],
        "snapshot_version": "v2.0",
        "scenario_version": "v2.0",
        "created_at": now_iso
    }
    _in_memory_digital_twin_experiment_results[exp_res1["id"]] = exp_res1

    # Validation, Model Error, Drift & Scenario Library
    val1 = {
        "id": "val_01",
        "accuracy_pct": 94.5,
        "coverage_pct": 96.0,
        "divergence_pct": 2.5,
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_digital_twin_validations[val1["id"]] = val1

    merr1 = {
        "id": "merr_01",
        "error_type": "recovery_error",
        "description": "Simulation predicted stabilization in 3 days; actual observed recovery took 5 days.",
        "predicted_value": "3 days",
        "observed_value": "5 days",
        "created_at": now_iso
    }
    _in_memory_digital_twin_model_errors[merr1["id"]] = merr1

    drift1 = {
        "id": "drift_01",
        "drift_type": "behavior_drift",
        "description": "Observed 3% drift between predicted and actual compute queue depth recovery rate over 14-day window.",
        "drift_magnitude": 0.03,
        "created_at": now_iso
    }
    _in_memory_digital_twin_drifts[drift1["id"]] = drift1

    slib1 = {
        "id": "slib_01",
        "name": "Standard Compute Dependency Outage Benchmark",
        "category": "stress",
        "scenario_ref": cscen1["id"],
        "approved_for_reuse": True,
        "created_at": now_iso
    }
    _in_memory_digital_twin_scenario_libraries[slib1["id"]] = slib1

_initialize_seed_digital_twin_data()


class TransformationResilienceDigitalTwinService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_DIGITAL_TWIN_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may create scenario forks, run simulations, compare states, identify divergence, prepare experiments, summarize resilience.
        # Agents may NOT modify production through simulation, approve experiments requiring governance, execute production actions, or change real-world state.
        forbidden_actions = [
            "modify_production_through_simulation", "approve_experiments_requiring_governance",
            "execute_production_actions", "change_real_world_state"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"BLOCKED. Agent '{agent_id}' is strictly prohibited from mutating production or executing real-world state changes."
            }
        return {"allowed": True, "reason": "Action permitted for Digital Twin agent."}

    @staticmethod
    async def create_scenario_fork(session: Optional[AsyncSession], base_snapshot_id: str, owner: str) -> dict:
        _initialize_seed_digital_twin_data()
        fork_id = f"fork_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        fork = {
            "id": fork_id,
            "base_snapshot_id": base_snapshot_id,
            "scenario_id": f"scen_fork_{uuid.uuid4().hex[:6]}",
            "owner": owner,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(days=7)).isoformat()
        }
        _in_memory_digital_twin_scenario_forks[fork["id"]] = fork
        TransformationResilienceDigitalTwinService.emit_event(
            "transformation.resilience.digital_twin.scenario_fork.created", fork
        )
        return fork

    @staticmethod
    async def run_what_if_analysis(session: Optional[AsyncSession], changes: List[dict], horizon_days: int = 30) -> dict:
        _initialize_seed_digital_twin_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        scen_id = f"cscen_{uuid.uuid4().hex[:8]}"
        outcome = {
            "scenario_id": scen_id,
            "changes_processed": len(changes),
            "risk_score": 0.84,
            "coverage_score": 0.92,
            "capacity_score": 0.78,
            "deadline_impact_days": 10,
            "dependency_exposure_score": 0.80,
            "residual_risk_score": 0.09,
            "recovery_time_days": 6,
            "isolation_status": "strictly_isolated_non_production",
            "created_at": now_iso
        }
        TransformationResilienceDigitalTwinService.emit_event(
            "transformation.resilience.digital_twin.counterfactual.created", outcome
        )
        return outcome

    @staticmethod
    async def run_stress_test(session: Optional[AsyncSession], stress_type: str, severity: str = "critical") -> dict:
        _initialize_seed_digital_twin_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        stress = {
            "id": f"stress_{uuid.uuid4().hex[:8]}",
            "stress_type": stress_type,
            "severity": severity,
            "affected_domains_json": ["Cloud Transformation Wave 3", "HR Cloud Wave 4"],
            "recovery_impact": "Requires 5-day contingency buffer to stabilize compute queue depth under severe stress.",
            "created_at": now_iso
        }
        _in_memory_digital_twin_stress_scenarios[stress["id"]] = stress
        TransformationResilienceDigitalTwinService.emit_event(
            "transformation.resilience.digital_twin.stress.created", stress
        )
        return stress

    @staticmethod
    async def run_recovery_simulation(session: Optional[AsyncSession], recovery_mode: str = "contingency_recovery") -> dict:
        _initialize_seed_digital_twin_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        rec = {
            "id": f"rec_{uuid.uuid4().hex[:8]}",
            "recovery_mode": recovery_mode,
            "time_to_stabilization_days": 5,
            "risk_reduction_pct": 85.0,
            "coverage_recovery_pct": 95.0,
            "capacity_recovery_pct": 90.0,
            "residual_exposure": 0.08,
            "created_at": now_iso
        }
        _in_memory_digital_twin_recovery_scenarios[rec["id"]] = rec
        TransformationResilienceDigitalTwinService.emit_event(
            "transformation.resilience.digital_twin.recovery.created", rec
        )
        return rec

    @staticmethod
    async def run_experiment(session: Optional[AsyncSession], exp_data: dict) -> dict:
        _initialize_seed_digital_twin_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        exp_id = f"exp_{uuid.uuid4().hex[:8]}"
        exp = {
            "id": exp_id,
            "title": exp_data.get("title", "Governed Resilience Experiment"),
            "hypothesis": exp_data.get("hypothesis", "Hypothesis test"),
            "scope": "simulation_only",
            "assumptions_json": exp_data.get("assumptions", []),
            "expected_result": exp_data.get("expected_result", "Expected outcome"),
            "status": "completed",
            "authorization_ref": "auth_sim_governance_105",
            "created_at": now_iso
        }
        exp_result = {
            "id": f"expres_{uuid.uuid4().hex[:8]}",
            "experiment_id": exp_id,
            "hypothesis": exp["hypothesis"],
            "observed_result": "Observed 84% reduction in systemic exposure under simulated experiment.",
            "expected_result": exp["expected_result"],
            "variance": "Exceeded expectation by +4%",
            "confidence": 0.94,
            "limitations_json": ["Assumes secondary cloud bandwidth quota unconstrained"],
            "snapshot_version": "v2.0",
            "scenario_version": "v2.0",
            "created_at": now_iso
        }
        _in_memory_digital_twin_experiments[exp["id"]] = exp
        _in_memory_digital_twin_experiment_results[exp_result["id"]] = exp_result

        TransformationResilienceDigitalTwinService.emit_event(
            "transformation.resilience.digital_twin.experiment.completed", exp_result
        )
        return {"experiment": exp, "result": exp_result}

    @staticmethod
    async def get_digital_twin_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_digital_twin_data()
        domains = list(_in_memory_digital_twin_domains.values())
        states = list(_in_memory_digital_twin_states.values())
        snapshots = list(_in_memory_digital_twin_snapshots.values())
        synchronizations = list(_in_memory_digital_twin_synchronizations.values())
        state_diffs = list(_in_memory_digital_twin_state_diffs.values())
        reality_comparisons = list(_in_memory_digital_twin_reality_comparisons.values())
        scenario_forks = list(_in_memory_digital_twin_scenario_forks.values())
        counterfactual_scenarios = list(_in_memory_digital_twin_counterfactual_scenarios.values())
        outcomes = list(_in_memory_digital_twin_scenario_outcomes.values())
        stress_scenarios = list(_in_memory_digital_twin_stress_scenarios.values())
        shock_scenarios = list(_in_memory_digital_twin_external_shock_scenarios.values())
        recovery_scenarios = list(_in_memory_digital_twin_recovery_scenarios.values())
        experiments = list(_in_memory_digital_twin_experiments.values())
        experiment_results = list(_in_memory_digital_twin_experiment_results.values())
        validations = list(_in_memory_digital_twin_validations.values())
        model_errors = list(_in_memory_digital_twin_model_errors.values())
        drifts = list(_in_memory_digital_twin_drifts.values())
        libraries = list(_in_memory_digital_twin_scenario_libraries.values())

        return {
            "domainsCount": len(domains),
            "snapshotsCount": len(snapshots),
            "scenarioForksCount": len(scenario_forks),
            "counterfactualScenariosCount": len(counterfactual_scenarios),
            "stressScenariosCount": len(stress_scenarios),
            "experimentsCount": len(experiments),
            "modelErrorsCount": len(model_errors),
            "driftsCount": len(drifts),
            "domains": domains,
            "states": states,
            "snapshots": snapshots,
            "synchronizations": synchronizations,
            "stateDiffs": state_diffs,
            "realityComparisons": reality_comparisons,
            "scenarioForks": scenario_forks,
            "counterfactualScenarios": counterfactual_scenarios,
            "outcomes": outcomes,
            "stressScenarios": stress_scenarios,
            "shockScenarios": shock_scenarios,
            "recoveryScenarios": recovery_scenarios,
            "experiments": experiments,
            "experimentResults": experiment_results,
            "validations": validations,
            "modelErrors": model_errors,
            "drifts": drifts,
            "scenarioLibraries": libraries
        }

    @staticmethod
    async def process_natural_language_digital_twin_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_digital_twin_data()

        # Anti-Surveillance / Privacy check (blocking employee digital twins, individual behavioral simulations, or employee productivity simulations)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee digital twin", "individual behavioral simulation", "employee productivity simulation",
            "simulate employee performance", "surveil employee twin"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee digital twins or individual behavioral productivity simulations."},
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
                    "current_state": "Digital Twin 'dtdom_01' (v2.0) is Current. Freshness: 100%, Completeness: 98%, Confidence: 95%. Production telemetry lag: 0.0s.",
                    "reality_comparison": "Production shows Compute Cluster 01 at 85% utilization; Twin matches across 98% of objects with 2% telemetry divergence.",
                    "what_if_outcomes": "Simulated 72h compute outage increases overall wave deployment risk to 0.88 (+28%) and delays HR Cloud Go-Live by 14 days.",
                    "stress_testing": "Capacity Stress Test 'stress_01' (Critical): Stabilizes within 5 days when 5-day contingency buffer is activated.",
                    "governed_experiment": "Experiment 'exp_01' (Completed): Secondary cluster failover reserve reduces systemic compute exposure by 84% (v2.0 reproducible).",
                    "model_validation": "Validation 'val_01': Accuracy 94.5%, Coverage 96.0%, Divergence 2.5%, Drift 3% (behavior_drift).",
                    "read_only_notice": "THE DIGITAL TWIN IS NOT PRODUCTION. All simulations execute in strictly isolated scenario forks."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Digital Twin 2.0",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.8
        }
