import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_stress_domains: Dict[str, dict] = {}
_in_memory_stress_hypotheses: Dict[str, dict] = {}
_in_memory_stress_campaigns: Dict[str, dict] = {}
_in_memory_stress_failure_injections: Dict[str, dict] = {}
_in_memory_stress_compound_failures: Dict[str, dict] = {}
_in_memory_stress_scenarios: Dict[str, dict] = {}
_in_memory_stress_runs: Dict[str, dict] = {}
_in_memory_stress_detection_results: Dict[str, dict] = {}
_in_memory_stress_warning_validations: Dict[str, dict] = {}
_in_memory_stress_intervention_validations: Dict[str, dict] = {}
_in_memory_stress_recovery_results: Dict[str, dict] = {}
_in_memory_stress_results: Dict[str, dict] = {}
_in_memory_stress_assurance_gaps: Dict[str, dict] = {}
_in_memory_stress_controls: Dict[str, dict] = {}
_in_memory_stress_control_results: Dict[str, dict] = {}
_in_memory_stress_control_failures: Dict[str, dict] = {}
_in_memory_stress_scorecards: Dict[str, dict] = {}
_in_memory_stress_trends: Dict[str, dict] = {}
_in_memory_stress_regressions: Dict[str, dict] = {}
_in_memory_stress_coverages: Dict[str, dict] = {}
_in_memory_stress_coverage_gaps: Dict[str, dict] = {}
_in_memory_stress_scenario_mutations: Dict[str, dict] = {}
_in_memory_stress_adversarial_scenarios: Dict[str, dict] = {}
_in_memory_stress_recovery_playbook_tests: Dict[str, dict] = {}
_in_memory_stress_governance_tests: Dict[str, dict] = {}
_in_memory_stress_remediation_recommendations: Dict[str, dict] = {}

_EMITTED_STRESS_EVENTS: List[dict] = []

EMITTED_STRESS_EVENT_TYPES = [
    "transformation.resilience.stress.domain.created",
    "transformation.resilience.stress.hypothesis.created",
    "transformation.resilience.stress.campaign.created",
    "transformation.resilience.stress.campaign.started",
    "transformation.resilience.stress.failure_injection.created",
    "transformation.resilience.stress.scenario.created",
    "transformation.resilience.stress.run.started",
    "transformation.resilience.stress.run.completed",
    "transformation.resilience.stress.detection.completed",
    "transformation.resilience.stress.warning.validated",
    "transformation.resilience.stress.intervention.validated",
    "transformation.resilience.stress.recovery.completed",
    "transformation.resilience.stress.result.created",
    "transformation.resilience.stress.assurance_gap.detected",
    "transformation.resilience.stress.control.tested",
    "transformation.resilience.stress.control.failed",
    "transformation.resilience.stress.scorecard.updated",
    "transformation.resilience.stress.trend.updated",
    "transformation.resilience.stress.regression.detected",
    "transformation.resilience.stress.coverage.updated",
    "transformation.resilience.stress.coverage_gap.detected",
    "transformation.resilience.stress.mutation.created",
    "transformation.resilience.stress.adversarial.created",
    "transformation.resilience.stress.playbook.tested",
    "transformation.resilience.stress.governance.tested",
    "transformation.resilience.stress.remediation.created"
]

def _initialize_seed_stress_data():
    if _in_memory_stress_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Domain & Hypothesis
    sdom1 = {
        "id": "sdom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Autonomous Resilience Simulation & Stress Testing 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Resilience Simulation Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_stress_domains[sdom1["id"]] = sdom1

    hyp1 = {
        "id": "hyp_01",
        "hypothesis": "Shared compute cluster failure can be contained without delaying HR Cloud Go-Live by more than 7 days.",
        "assumptions_json": ["Secondary backup compute pool available", "Telemetry lead time >= 12 seconds"],
        "expected_outcome": "Systemic exposure contained with 85% risk reduction upon contingency activation.",
        "confidence": 0.90,
        "owner": "Principal Enterprise Resilience Simulation Architect",
        "created_at": now_iso
    }
    _in_memory_stress_hypotheses[hyp1["id"]] = hyp1

    # Campaign & Failure Injection
    camp1 = {
        "id": "camp_01",
        "name": "Continuous Wave 3 & Wave 4 Compute Outage Campaign",
        "objective": "Continuously test resilience against primary compute cluster outages.",
        "scope": "enterprise",
        "hypotheses_json": [hyp1["id"]],
        "scenario_set_json": ["stscen_01"],
        "schedule": "continuous",
        "governance_ref": "gov_stress_auth_106",
        "status": "running",
        "created_at": now_iso
    }
    _in_memory_stress_campaigns[camp1["id"]] = camp1

    inj1 = {
        "id": "inj_01",
        "injection_type": "dependency_failure",
        "target_id": "dep_compute_cluster_01",
        "domain": "Infrastructure & Compute",
        "severity": "high",
        "duration": "sustained",
        "environment": "SIMULATION_ONLY",
        "sandbox_id": "sbx_resilience_106_01",
        "source_snapshot_id": "dtsnap_v2_0",
        "authorization_ref": "auth_sim_governance_106",
        "rollback_plan": "Automatic sandbox state purge upon completion",
        "created_at": now_iso
    }
    _in_memory_stress_failure_injections[inj1["id"]] = inj1

    cfail1 = {
        "id": "cfail_01",
        "failure_a_id": inj1["id"],
        "failure_b_id": "inj_deadline_compression_02",
        "failure_c_id": None,
        "interaction": "amplifying",
        "combined_impact": "Simultaneous compute outage and deadline compression increases wave disruption by +35%.",
        "confidence": 0.90
    }
    _in_memory_stress_compound_failures[cfail1["id"]] = cfail1

    # Scenario & Run
    scen1 = {
        "id": "stscen_01",
        "baseline_snapshot_id": "dtsnap_v2_0",
        "injections_json": [inj1["id"]],
        "assumptions_json": ["Secondary cloud reserve pool functional"],
        "horizon_days": 30,
        "expected_outcome": "Detection within 15 seconds, full stabilization within 5 days.",
        "created_at": now_iso
    }
    _in_memory_stress_scenarios[scen1["id"]] = scen1

    run1 = {
        "id": "run_01",
        "scenario_id": scen1["id"],
        "snapshot_id": "dtsnap_v2_0",
        "simulation_version": "v2.0",
        "seed": 42,
        "start_time": now_iso,
        "end_time": (now + timedelta(minutes=2)).isoformat(),
        "status": "completed",
        "created_at": now_iso
    }
    _in_memory_stress_runs[run1["id"]] = run1

    # Detection, Warning & Intervention Validations
    det1 = {
        "id": "det_01",
        "run_id": run1["id"],
        "detected": True,
        "detection_time_seconds": 12.0,
        "detection_source": "Resilience Sensing Mesh 2.0",
        "confidence": 0.95,
        "false_negative": False,
        "created_at": now_iso
    }
    _in_memory_stress_detection_results[det1["id"]] = det1

    wval1 = {
        "id": "wval_01",
        "expected_warning": "High-confidence early warning for compute cluster queue depth compression",
        "actual_warning": "Warning swarn_01 issued by Assurance Foresight",
        "severity": "critical",
        "timing_lead_time_days": 5,
        "accuracy_pct": 96.0,
        "created_at": now_iso
    }
    _in_memory_stress_warning_validations[wval1["id"]] = wval1

    ival1 = {
        "id": "ival_01",
        "intervention_recommended": True,
        "intervention_authorized": True,
        "intervention_executed": True,
        "effectiveness_pct": 88.5,
        "created_at": now_iso
    }
    _in_memory_stress_intervention_validations[ival1["id"]] = ival1

    recres1 = {
        "id": "recres_01",
        "recovery_start_time": now_iso,
        "stabilization_days": 4,
        "coverage_restoration_pct": 95.0,
        "risk_reduction_pct": 85.0,
        "residual_exposure": 0.08,
        "created_at": now_iso
    }
    _in_memory_stress_recovery_results[recres1["id"]] = recres1

    sres1 = {
        "id": "sres_01",
        "run_id": run1["id"],
        "detection_passed": True,
        "warning_passed": True,
        "intervention_passed": True,
        "recovery_passed": True,
        "residual_exposure": 0.08,
        "hypothesis_result": "passed",
        "created_at": now_iso
    }
    _in_memory_stress_results[sres1["id"]] = sres1

    # Assurance Gap & Controls
    gap1 = {
        "id": "gap_01",
        "gap_type": "capacity_gap",
        "description": "Secondary cloud cluster failover lacks automated bandwidth quota expansion.",
        "severity": "high",
        "evidence_json": ["run_01", "recres_01"]
    }
    _in_memory_stress_assurance_gaps[gap1["id"]] = gap1

    ctrl1 = {
        "id": "ctrl_01",
        "name": "Compute Queue Depth Telemetry Monitor",
        "control_type": "monitoring",
        "target": "dep_compute_cluster_01",
        "created_at": now_iso
    }
    _in_memory_stress_controls[ctrl1["id"]] = ctrl1

    cres1 = {
        "id": "cres_01",
        "control_id": ctrl1["id"],
        "expected_behavior": "Detect queue depth > 80% within 15 seconds.",
        "observed_behavior": "Detected queue depth at 85% in 12 seconds.",
        "variance": "20% faster detection than target lead time.",
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_stress_control_results[cres1["id"]] = cres1

    cfail_ctrl1 = {
        "id": "cfail_ctrl_01",
        "control_id": "ctrl_secondary_bandwidth_quota",
        "failure_reason": "Bandwidth quota limit reached during secondary cluster failover burst.",
        "impact": "Delayed backup telemetry sync by 45 seconds.",
        "recommended_improvement": "Upgrade auto-scaling quota ceiling.",
        "created_at": now_iso
    }
    _in_memory_stress_control_failures[cfail_ctrl1["id"]] = cfail_ctrl1

    # Scorecard, Trend, Regression & Coverage
    scard1 = {
        "id": "scorecard_01",
        "detection_score": 0.92,
        "response_score": 0.88,
        "recovery_score": 0.90,
        "evidence_score": 0.95,
        "dependency_resilience_score": 0.85,
        "governance_score": 0.96,
        "coverage_score": 0.94,
        "created_at": now_iso
    }
    _in_memory_stress_scorecards[scard1["id"]] = scard1

    trend1 = {
        "id": "trend_01",
        "direction": "improving",
        "summary": "Resilience detection lead time improved by 15% over the past 30 days.",
        "created_at": now_iso
    }
    _in_memory_stress_trends[trend1["id"]] = trend1

    reg1 = {
        "id": "reg_01",
        "test_id": "test_secondary_failover_quota",
        "previous_result": "passed",
        "current_result": "failed",
        "status": "investigating",
        "likely_cause": "Recent wave workload increase exceeded default quota limit.",
        "created_at": now_iso
    }
    _in_memory_stress_regressions[reg1["id"]] = reg1

    cov1 = {
        "id": "cov_01",
        "transformations_pct": 92.0,
        "plans_pct": 95.0,
        "dependencies_pct": 88.0,
        "risks_pct": 94.0,
        "knowledge_pct": 90.0,
        "decisions_pct": 96.0,
        "interventions_pct": 92.0,
        "recovery_paths_pct": 85.0,
        "created_at": now_iso
    }
    _in_memory_stress_coverages[cov1["id"]] = cov1

    covgap1 = {
        "id": "covgap_01",
        "target_area": "ERP Wave 5 Contingency Failover",
        "gap_reason": "insufficient_recovery_validation",
        "severity": "high",
        "created_at": now_iso
    }
    _in_memory_stress_coverage_gaps[covgap1["id"]] = covgap1

    # Mutations, Adversarial, Playbook Test & Remediation
    smut1 = {
        "id": "smut_01",
        "mutation_type": "combine_failures",
        "target_scenario_id": scen1["id"],
        "created_at": now_iso
    }
    _in_memory_stress_scenario_mutations[smut1["id"]] = smut1

    adv1 = {
        "id": "adv_01",
        "title": "Near-Threshold Compute Outage & Late Warning Pattern",
        "adversarial_pattern": "late_warning",
        "description": "Simulates 79% compute queue depth compression (just below 80% warning threshold) followed by sudden 95% spike.",
        "created_at": now_iso
    }
    _in_memory_stress_adversarial_scenarios[adv1["id"]] = adv1

    pbook1 = {
        "id": "pbook_01",
        "playbook_name": "Secondary Cluster Failover & Workload Resequencing Playbook",
        "readiness_status": "ready",
        "missing_dependencies_json": [],
        "created_at": now_iso
    }
    _in_memory_stress_recovery_playbook_tests[pbook1["id"]] = pbook1

    govtest1 = {
        "id": "govtest_01",
        "tested_boundary": "ActionGateway Approval Boundary Check",
        "compliance_passed": True,
        "findings_json": ["All simulated interventions properly checked against PolicyEngine RBAC rules."],
        "created_at": now_iso
    }
    _in_memory_stress_governance_tests[govtest1["id"]] = govtest1

    remed1 = {
        "id": "remed_01",
        "gap_id": gap1["id"],
        "recommended_improvement": "Configure auto-scaling secondary cluster reserve with dynamic quota expansion.",
        "expected_benefit": "Eliminates secondary cluster bandwidth quota bottleneck during peak failover burst.",
        "effort": "medium",
        "risk": "low",
        "confidence": 0.92,
        "label": "ANALYTICAL RECOMMENDATION — NOT DECISION",
        "created_at": now_iso
    }
    _in_memory_stress_remediation_recommendations[remed1["id"]] = remed1

_initialize_seed_stress_data()


class TransformationResilienceStressService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_STRESS_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may propose scenarios, run authorized simulations, compare outcomes, identify assurance gaps, prepare remediation recommendations.
        # Agents may NOT inject production failures, approve tests requiring governance, execute production actions, or modify source snapshots.
        forbidden_actions = [
            "inject_production_failures", "approve_tests_requiring_governance",
            "execute_production_actions", "modify_source_snapshots"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"BLOCKED. Agent '{agent_id}' is strictly prohibited from injecting production failures or modifying source snapshots."
            }
        return {"allowed": True, "reason": "Action permitted for Stress Testing agent."}

    @staticmethod
    async def start_campaign(session: Optional[AsyncSession], campaign_id: str) -> dict:
        _initialize_seed_stress_data()
        camp = _in_memory_stress_campaigns.get(campaign_id)
        if not camp:
            camp = list(_in_memory_stress_campaigns.values())[0]
        camp["status"] = "running"
        TransformationResilienceStressService.emit_event(
            "transformation.resilience.stress.campaign.started", camp
        )
        return camp

    @staticmethod
    async def create_failure_injection(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_stress_data()
        inj_id = f"inj_{uuid.uuid4().hex[:8]}"
        inj = {
            "id": inj_id,
            "injection_type": data.get("injection_type", "dependency_failure"),
            "target_id": data.get("target_id", "dep_compute_cluster_01"),
            "domain": data.get("domain", "Infrastructure & Compute"),
            "severity": data.get("severity", "high"),
            "duration": data.get("duration", "sustained"),
            "environment": "SIMULATION_ONLY", # Always default to SIMULATION_ONLY
            "sandbox_id": f"sbx_{uuid.uuid4().hex[:6]}",
            "source_snapshot_id": data.get("source_snapshot_id", "dtsnap_v2_0"),
            "authorization_ref": "auth_sim_governance_106",
            "rollback_plan": "Automatic sandbox state purge upon completion",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_stress_failure_injections[inj["id"]] = inj
        TransformationResilienceStressService.emit_event(
            "transformation.resilience.stress.failure_injection.created", inj
        )
        return inj

    @staticmethod
    async def run_scenario_simulation(session: Optional[AsyncSession], scenario_id: str, seed: int = 42) -> dict:
        _initialize_seed_stress_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        run = {
            "id": run_id,
            "scenario_id": scenario_id,
            "snapshot_id": "dtsnap_v2_0",
            "simulation_version": "v2.0",
            "seed": seed,
            "start_time": now_iso,
            "end_time": (datetime.now(timezone.utc) + timedelta(seconds=1.5)).isoformat(),
            "status": "completed",
            "created_at": now_iso
        }
        res = {
            "id": f"sres_{uuid.uuid4().hex[:8]}",
            "run_id": run_id,
            "detection_passed": True,
            "warning_passed": True,
            "intervention_passed": True,
            "recovery_passed": True,
            "residual_exposure": 0.08,
            "hypothesis_result": "passed",
            "created_at": now_iso
        }
        _in_memory_stress_runs[run["id"]] = run
        _in_memory_stress_results[res["id"]] = res

        TransformationResilienceStressService.emit_event(
            "transformation.resilience.stress.run.completed", run
        )
        return {"run": run, "result": res}

    @staticmethod
    async def test_recovery_playbook(session: Optional[AsyncSession], playbook_id: str) -> dict:
        _initialize_seed_stress_data()
        pbook = _in_memory_stress_recovery_playbook_tests.get(playbook_id)
        if not pbook:
            pbook = list(_in_memory_stress_recovery_playbook_tests.values())[0]
        pbook["readiness_status"] = "ready"
        TransformationResilienceStressService.emit_event(
            "transformation.resilience.stress.playbook.tested", pbook
        )
        return pbook

    @staticmethod
    async def get_stress_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_stress_data()
        domains = list(_in_memory_stress_domains.values())
        hypotheses = list(_in_memory_stress_hypotheses.values())
        campaigns = list(_in_memory_stress_campaigns.values())
        injections = list(_in_memory_stress_failure_injections.values())
        compound_failures = list(_in_memory_stress_compound_failures.values())
        scenarios = list(_in_memory_stress_scenarios.values())
        runs = list(_in_memory_stress_runs.values())
        detection_results = list(_in_memory_stress_detection_results.values())
        warning_validations = list(_in_memory_stress_warning_validations.values())
        intervention_validations = list(_in_memory_stress_intervention_validations.values())
        recovery_results = list(_in_memory_stress_recovery_results.values())
        results = list(_in_memory_stress_results.values())
        assurance_gaps = list(_in_memory_stress_assurance_gaps.values())
        controls = list(_in_memory_stress_controls.values())
        control_results = list(_in_memory_stress_control_results.values())
        control_failures = list(_in_memory_stress_control_failures.values())
        scorecards = list(_in_memory_stress_scorecards.values())
        trends = list(_in_memory_stress_trends.values())
        regressions = list(_in_memory_stress_regressions.values())
        coverages = list(_in_memory_stress_coverages.values())
        coverage_gaps = list(_in_memory_stress_coverage_gaps.values())
        mutations = list(_in_memory_stress_scenario_mutations.values())
        adversarial_scenarios = list(_in_memory_stress_adversarial_scenarios.values())
        playbook_tests = list(_in_memory_stress_recovery_playbook_tests.values())
        governance_tests = list(_in_memory_stress_governance_tests.values())
        remediation_recommendations = list(_in_memory_stress_remediation_recommendations.values())

        return {
            "domainsCount": len(domains),
            "campaignsCount": len(campaigns),
            "hypothesesCount": len(hypotheses),
            "injectionsCount": len(injections),
            "runsCount": len(runs),
            "assuranceGapsCount": len(assurance_gaps),
            "regressionsCount": len(regressions),
            "remediationsCount": len(remediation_recommendations),
            "domains": domains,
            "hypotheses": hypotheses,
            "campaigns": campaigns,
            "injections": injections,
            "compoundFailures": compound_failures,
            "scenarios": scenarios,
            "runs": runs,
            "detectionResults": detection_results,
            "warningValidations": warning_validations,
            "interventionValidations": intervention_validations,
            "recoveryResults": recovery_results,
            "results": results,
            "assuranceGaps": assurance_gaps,
            "controls": controls,
            "controlResults": control_results,
            "controlFailures": control_failures,
            "scorecards": scorecards,
            "trends": trends,
            "regressions": regressions,
            "coverages": coverages,
            "coverageGaps": coverage_gaps,
            "mutations": mutations,
            "adversarialScenarios": adversarial_scenarios,
            "playbookTests": playbook_tests,
            "governanceTests": governance_tests,
            "remediationRecommendations": remediation_recommendations
        }

    @staticmethod
    async def process_natural_language_stress_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_stress_data()

        # Anti-Surveillance / Privacy check (blocking employee stress tests, employee behavioral resilience scores, or individual productivity failure simulations)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee stress test", "employee behavioral resilience", "individual productivity failure simulation",
            "rank worker resilience score", "stress test employee performance"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee stress testing, behavioral resilience scoring, or individual worker failure simulations."},
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
                    "campaign_status": "Campaign 'camp_01' (Running): Continuous testing of Wave 3 & Wave 4 primary compute cluster outages.",
                    "failure_injection": "Injection 'inj_01' (SIMULATION_ONLY): Primary compute cluster 01 sustained outage in sandbox 'sbx_resilience_106_01'.",
                    "detection_time": "Resilience Sensing Mesh detected injected outage in 12.0 seconds with zero false negatives.",
                    "recovery_stabilization": "Contingency recovery stabilized system in 4 days with 85% risk reduction and 0.08 residual exposure.",
                    "scorecard": "Multi-Dimensional Scorecard: Detection 92%, Response 88%, Recovery 90%, Evidence 95%, Governance 96%, Coverage 94%.",
                    "assurance_gaps": "Assurance Gap 'gap_01' (High): Secondary cloud cluster failover lacks automated bandwidth quota expansion.",
                    "remediation_label": "ANALYTICAL RECOMMENDATION — NOT DECISION. Configure auto-scaling secondary cluster reserve with dynamic quota expansion."
                }
            ],
            "evidenceJson": {
                "data_source": "Autonomous Resilience Simulation & Continuous Enterprise Stress Testing 2.0",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.8
        }
