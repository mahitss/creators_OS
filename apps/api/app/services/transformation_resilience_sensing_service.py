import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_sensing_domains: Dict[str, dict] = {}
_in_memory_observations: Dict[str, dict] = {}
_in_memory_observation_qualities: Dict[str, dict] = {}
_in_memory_normalizations: Dict[str, dict] = {}
_in_memory_dynamic_baselines: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}
_in_memory_structural_changes: Dict[str, dict] = {}
_in_memory_alert_evaluations: Dict[str, dict] = {}
_in_memory_sensing_warnings: Dict[str, dict] = {}
_in_memory_signal_correlations: Dict[str, dict] = {}
_in_memory_state_changes: Dict[str, dict] = {}
_in_memory_trends: Dict[str, dict] = {}
_in_memory_forecasts: Dict[str, dict] = {}
_in_memory_assumptions: Dict[str, dict] = {}
_in_memory_assumption_drifts: Dict[str, dict] = {}
_in_memory_investment_review_triggers: Dict[str, dict] = {}
_in_memory_portfolio_resilience_states: Dict[str, dict] = {}

_EMITTED_SENSING_EVENTS: List[dict] = []

EMITTED_SENSING_EVENT_TYPES = [
    "transformation.resilience.sensing.domain.created",
    "transformation.resilience.observation.created",
    "transformation.resilience.observation.quality.updated",
    "transformation.resilience.signal.normalized",
    "transformation.resilience.baseline.created",
    "transformation.resilience.baseline.versioned",
    "transformation.resilience.drift.detected",
    "transformation.resilience.structural_change.detected",
    "transformation.resilience.alert.evaluated",
    "transformation.resilience.warning.created",
    "transformation.resilience.signal.correlated",
    "transformation.resilience.exposure.updated",
    "transformation.resilience.state.changed",
    "transformation.resilience.trend.updated",
    "transformation.resilience.forecast.created",
    "transformation.resilience.forecast.validated",
    "transformation.resilience.assumption.updated",
    "transformation.resilience.assumption.drifted",
    "transformation.resilience.scenario.invalidated",
    "transformation.resilience.investment.review_triggered",
    "transformation.resilience.decision.review_triggered",
    "transformation.resilience.attention.created"
]

def _initialize_seed_resilience_sensing_data():
    if _in_memory_sensing_domains:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Domain
    dom1 = {
        "id": "sens_dom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Resilience Sensing 2.0 Domain",
        "scope": "enterprise",
        "owner": "Principal Resilience Sensing Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_sensing_domains[dom1["id"]] = dom1

    # Observation & Quality
    obs1 = {
        "id": "obs_01",
        "domain_id": dom1["id"],
        "source": "EventMesh.IdentityGateway",
        "metric": "OAuth Token Resolution Latency (P99)",
        "value": 142.5,
        "timestamp": now_iso,
        "confidence": 0.96,
        "freshness": 1.0,
        "scope": "portfolio"
    }
    _in_memory_observations[obs1["id"]] = obs1

    obs_qual1 = {
        "id": "obs_qual_01",
        "observation_id": obs1["id"],
        "completeness": 0.98,
        "freshness": 1.0,
        "consistency": 0.95,
        "reliability": 0.96
    }
    _in_memory_observation_qualities[obs_qual1["id"]] = obs_qual1

    # Normalization & Dynamic Baseline
    norm1 = {
        "id": "norm_01",
        "domain_id": dom1["id"],
        "source_metric": "OAuth Token Resolution Latency (P99)",
        "normalized_dimension": "robustness",
        "normalized_score": 0.88
    }
    _in_memory_normalizations[norm1["id"]] = norm1

    base1 = {
        "id": "base_01",
        "domain_id": dom1["id"],
        "version": "v1.2",
        "effective_period": "2026-Q3",
        "change_reason": "Incorporated Active-Active IAM Redundancy Baseline",
        "approval_context_json": {"approved_by": "Enterprise Resilience Board", "approval_id": "appr_9921"},
        "baseline_metrics_json": {"target_robustness": 0.95, "max_acceptable_latency_ms": 100.0}
    }
    _in_memory_dynamic_baselines[base1["id"]] = base1

    # Drift & Structural Change & Alert Evaluation
    drift1 = {
        "id": "drift_01",
        "domain_id": dom1["id"],
        "drift_type": "persistent",
        "metric_name": "Shared Identity Gateway Latency",
        "deviation_pct": 8.4,
        "severity": "medium",
        "detected_at": now_iso
    }
    _in_memory_drifts[drift1["id"]] = drift1

    schange1 = {
        "id": "schange_01",
        "domain_id": dom1["id"],
        "change_type": "vendor_concentration_increased",
        "affected_scope_json": ["Wave 2 FinOps", "Wave 3 SSO", "Wave 4 HR Cloud"],
        "materiality": "material",
        "detected_at": now_iso
    }
    _in_memory_structural_changes[schange1["id"]] = schange1

    aeval1 = {
        "id": "aeval_01",
        "domain_id": dom1["id"],
        "condition_name": "Shared Identity Concentration Exceeded 90%",
        "persistence_count": 4,
        "corroboration_score": 0.94,
        "actionable": True
    }
    _in_memory_alert_evaluations[aeval1["id"]] = aeval1

    # Sensing Warning & Signal Correlation
    warn1 = {
        "id": "swarn_01",
        "domain_id": dom1["id"],
        "condition": "IAM OAuth Gateway Latency Degradation & Senior Security Engineer Capacity Contention",
        "severity": "high",
        "confidence": 0.95,
        "affected_scope_json": ["wave_02_finops", "wave_03_sso"],
        "recommended_review": "Initiate Portfolio Resilience Investment Review for pinv_01 Active-Active deploy.",
        "status": "active"
    }
    _in_memory_sensing_warnings[warn1["id"]] = warn1

    corr1 = {
        "id": "scorr_01",
        "domain_id": dom1["id"],
        "signal_a": "OAuth Gateway Latency P99",
        "signal_b": "Senior IAM Engineer Backlog",
        "relationship_type": "observed_correlation",
        "confidence": 0.93
    }
    _in_memory_signal_correlations[corr1["id"]] = corr1

    # State Change, Trend & Forecast
    stch1 = {
        "id": "stch_01",
        "domain_id": dom1["id"],
        "previous_state": "baseline_normal",
        "new_state": "degraded_observability",
        "evidence_json": {"latency_p99": 142.5, "drift_type": "persistent"},
        "confidence": 0.96,
        "timestamp": now_iso
    }
    _in_memory_state_changes[stch1["id"]] = stch1

    tr1 = {
        "id": "tr_01",
        "domain_id": dom1["id"],
        "dimension": "recoverability",
        "trend_direction": "deteriorating",
        "window": "30d"
    }
    _in_memory_trends[tr1["id"]] = tr1

    fc1 = {
        "id": "fc_01",
        "domain_id": dom1["id"],
        "target_metric": "Shared Dependency Recovery Margin",
        "forecast_value": 0.84,
        "uncertainty_json": {"lower_bound": 0.78, "upper_bound": 0.90, "confidence": 0.91},
        "created_at": now_iso
    }
    _in_memory_forecasts[fc1["id"]] = fc1

    # Assumption, Assumption Drift & Review Triggers
    ass1 = {
        "id": "ass_01",
        "domain_id": dom1["id"],
        "assumption_title": "Primary OAuth Auth Gateway SLA >= 99.99%",
        "source_context": "Wave 2 FinOps Architecture Design Doc",
        "status": "degraded"
    }
    _in_memory_assumptions[ass1["id"]] = ass1

    assdrift1 = {
        "id": "assdrift_01",
        "assumption_id": ass1["id"],
        "drift_description": "Actual primary OAuth Gateway availability dropped to 99.91% over 30d window.",
        "severity": "high",
        "affected_scenarios_json": ["scen_iam_failover_01", "scen_multi_failure_02"]
    }
    _in_memory_assumption_drifts[assdrift1["id"]] = assdrift1

    invtrig1 = {
        "id": "invtrig_01",
        "domain_id": dom1["id"],
        "affected_investment_id": "pinv_01",
        "reason": "Key assumption 'Primary Auth Gateway SLA >= 99.99%' drifted to degraded status.",
        "severity": "high",
        "review_deadline": "2026-Q3"
    }
    _in_memory_investment_review_triggers[invtrig1["id"]] = invtrig1

    pstate1 = {
        "id": "pstate_01",
        "domain_id": dom1["id"],
        "robustness": 0.94,
        "redundancy": 0.91,
        "recoverability": 0.95,
        "adaptability": 0.92,
        "optionality": 0.93,
        "observability": 0.96,
        "governability": 0.94,
        "updated_at": now_iso
    }
    _in_memory_portfolio_resilience_states[pstate1["id"]] = pstate1

_initialize_seed_resilience_sensing_data()


class TransformationResilienceSensingService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_SENSING_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from changing baselines, approving reviews, changing investments, executing interventions, or modifying governance
        forbidden_actions = [
            "change_baseline", "approve_review", "change_investment",
            "execute_intervention", "modify_governance", "allocate_budget",
            "cancel_transformation", "override_human_decision"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing non-read-only sensing action '{action}'. Action requires PolicyEngine authorization + human approval."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_sensing_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_sensing_data()
        domains = list(_in_memory_sensing_domains.values())
        observations = list(_in_memory_observations.values())
        qualities = list(_in_memory_observation_qualities.values())
        normalizations = list(_in_memory_normalizations.values())
        baselines = list(_in_memory_dynamic_baselines.values())
        drifts = list(_in_memory_drifts.values())
        structural_changes = list(_in_memory_structural_changes.values())
        evaluations = list(_in_memory_alert_evaluations.values())
        warnings = list(_in_memory_sensing_warnings.values())
        correlations = list(_in_memory_signal_correlations.values())
        state_changes = list(_in_memory_state_changes.values())
        trends = list(_in_memory_trends.values())
        forecasts = list(_in_memory_forecasts.values())
        assumptions = list(_in_memory_assumptions.values())
        assumption_drifts = list(_in_memory_assumption_drifts.values())
        investment_triggers = list(_in_memory_investment_review_triggers.values())
        portfolio_state = list(_in_memory_portfolio_resilience_states.values())[0] if _in_memory_portfolio_resilience_states else {}

        return {
            "domainsCount": len(domains),
            "observationsCount": len(observations),
            "activeDriftsCount": len(drifts),
            "structuralChangesCount": len(structural_changes),
            "activeWarningsCount": len(warnings),
            "signalCorrelationsCount": len(correlations),
            "assumptionDriftsCount": len(assumption_drifts),
            "investmentReviewTriggersCount": len(investment_triggers),
            "portfolioState": portfolio_state,
            "domains": domains,
            "observations": observations,
            "qualities": qualities,
            "normalizations": normalizations,
            "baselines": baselines,
            "drifts": drifts,
            "structuralChanges": structural_changes,
            "evaluations": evaluations,
            "warnings": warnings,
            "correlations": correlations,
            "stateChanges": state_changes,
            "trends": trends,
            "forecasts": forecasts,
            "assumptions": assumptions,
            "assumptionDrifts": assumption_drifts,
            "investmentTriggers": investment_triggers
        }

    @staticmethod
    async def acknowledge_review(session: Optional[AsyncSession], review_id: str) -> dict:
        _initialize_seed_resilience_sensing_data()
        trig = _in_memory_investment_review_triggers.get(review_id)
        if not trig:
            trig = {"id": review_id, "domain_id": "sens_dom_01", "severity": "high"}
        trig["acknowledged"] = True
        trig["acknowledged_at"] = datetime.now(timezone.utc).isoformat()
        _in_memory_investment_review_triggers[review_id] = trig
        TransformationResilienceSensingService.emit_event("transformation.resilience.investment.review_triggered", trig)
        return trig

    @staticmethod
    async def process_natural_language_sensing_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_sensing_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking individual employee resilience scores, worker performance predictions, or behavioral surveillance)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee resilience", "individual worker", "worker performance", "behavioral surveillance", "surveillance", "rank employee", "performance prediction"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee resilience scores, behavioral surveillance, or worker performance predictions."},
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
                    "sensing_domain": "Global Enterprise Transformation Resilience Sensing 2.0 Domain (sens_dom_01)",
                    "live_observation": "OAuth Token Resolution Latency P99 is 142.5ms (Signal Quality: 96% Reliability)",
                    "detected_drift": "Persistent drift detected on Shared Identity Gateway Latency (+8.4% deviation)",
                    "structural_change": "Material increase in vendor concentration detected across Wave 2 FinOps, Wave 3 SSO, and Wave 4 HR Cloud.",
                    "signal_correlation": "Observed correlation between OAuth Gateway Latency and Senior IAM Security Engineer backlog (Confidence: 93%). Note: Observed correlation does NOT confirm causation.",
                    "assumption_drift": "Assumption 'Primary OAuth Auth Gateway SLA >= 99.99%' status: DEGRADED (Actual 30d SLA: 99.91%).",
                    "investment_review_trigger": "Review triggered for pinv_01 Active-Active IAM Gateway due to assumption drift (Deadline: 2026-Q3).",
                    "portfolio_resilience_dimensions": "Robustness: 94%, Redundancy: 91%, Recoverability: 95%, Adaptability: 92%, Optionality: 93%, Observability: 96%, Governability: 94%"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Sensing 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 98.0
        }
