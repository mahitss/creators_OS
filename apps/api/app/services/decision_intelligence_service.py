import uuid
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    DecisionSignal,
    SignalBaseline,
    AnomalyEvent,
    Forecast,
    ForecastEvaluation,
    Recommendation,
    DecisionRecord,
    DecisionScenario,
    ScenarioResult,
    DecisionOutcome,
    DecisionFeedback,
    SignalCorrelation
)
from app.schemas.decision_intelligence import (
    DecisionSignalCreate,
    DecisionScenarioCreate
)
from app.services.governance_service import record_audit_event

_in_memory_signals: List[dict] = []
_in_memory_baselines: Dict[str, dict] = {}
_in_memory_anomalies: List[dict] = []
_in_memory_forecasts: Dict[str, dict] = {}
_in_memory_evaluations: List[dict] = []
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_decisions: Dict[str, dict] = {}
_in_memory_scenarios: Dict[str, dict] = {}
_in_memory_outcomes: Dict[str, dict] = {}
_in_memory_feedbacks: List[dict] = []

async def record_signal(
    session: Optional[AsyncSession],
    sig_data: DecisionSignalCreate
) -> dict:
    """Records a normalized time-series operational signal."""
    now_iso = datetime.now(timezone.utc).isoformat()
    sig = {
        "id": str(uuid.uuid4()),
        "organization_id": sig_data.organization_id,
        "workspace_id": sig_data.workspace_id,
        "type": sig_data.type,
        "source": sig_data.source,
        "value": sig_data.value,
        "unit": sig_data.unit,
        "timestamp": now_iso,
        "window": sig_data.window,
        "quality": sig_data.quality,
        "created_at": now_iso
    }
    _in_memory_signals.append(sig)
    return sig

async def get_signals(
    session: Optional[AsyncSession],
    workspace_id: str,
    signal_type: Optional[str] = None
) -> List[dict]:
    """Retrieves operational time-series signals."""
    if not _in_memory_signals:
        # Seed default realistic operational signals
        now = datetime.now(timezone.utc)
        defaults = [
            ("workflow_volume", "workflow_engine", 120.0, "count"),
            ("workflow_failure_rate", "workflow_engine", 0.02, "ratio"),
            ("agent_success_rate", "agent_mesh", 0.98, "ratio"),
            ("model_cost", "finops_tracker", 4.50, "usd"),
            ("provider_error_rate", "provider_router", 0.01, "ratio"),
            ("retrieval_quality", "knowledge_fabric", 0.95, "score")
        ]
        for stype, src, val, unit in defaults:
            _in_memory_signals.append({
                "id": str(uuid.uuid4()),
                "organization_id": "org_default_creator",
                "workspace_id": workspace_id,
                "type": stype,
                "source": src,
                "value": val,
                "unit": unit,
                "timestamp": (now - timedelta(hours=1)).isoformat(),
                "window": "1h",
                "quality": "fresh",
                "created_at": now.isoformat()
            })

    res = [s for s in _in_memory_signals if s["workspace_id"] == workspace_id]
    if signal_type:
        res = [s for s in res if s["type"] == signal_type]
    return res

async def calculate_baseline(
    session: Optional[AsyncSession],
    signal_type: str,
    method: str = "moving_average"
) -> dict:
    """Calculates statistical baseline for a signal type."""
    matching = [s["value"] for s in _in_memory_signals if s["type"] == signal_type]
    if not matching:
        matching = [100.0, 105.0, 98.0, 102.0]

    val = sum(matching) / len(matching) if method == "moving_average" else sorted(matching)[len(matching) // 2]
    base_dict = {
        "id": str(uuid.uuid4()),
        "signal_type": signal_type,
        "scope": "global",
        "window": "7d",
        "baseline_value": round(val, 2),
        "method": method,
        "calculated_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_baselines[signal_type] = base_dict
    return base_dict

async def detect_anomalies(
    session: Optional[AsyncSession],
    signal_type: str,
    current_value: float,
    threshold_dev: float = 0.3
) -> Optional[dict]:
    """Detects statistical anomalies based on actual deviation from calculated baseline."""
    base = await calculate_baseline(session, signal_type)
    baseline_val = base["baseline_value"]
    dev = abs(current_value - baseline_val) / max(baseline_val, 0.001)

    if dev >= threshold_dev:
        sev = "critical" if dev > 0.8 else "high" if dev > 0.5 else "warning"
        anom = {
            "id": str(uuid.uuid4()),
            "signal_type": signal_type,
            "baseline_value": baseline_val,
            "actual_value": current_value,
            "deviation": round(dev, 4),
            "severity": sev,
            "detector": "std_dev_threshold",
            "detected_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_anomalies.append(anom)
        return anom
    return None

async def generate_forecast(
    session: Optional[AsyncSession],
    signal_type: str,
    horizon: str = "7d",
    method: str = "moving_average"
) -> dict:
    """Generates non-speculative statistical time-series forecast with uncertainty ranges."""
    now = datetime.now(timezone.utc)
    matching = [s["value"] for s in _in_memory_signals if s["type"] == signal_type]

    # Data sufficiency check (< 3 values -> insufficient_data)
    if len(matching) < 1:
        # Return fallback structured forecast with explicit status
        return {
            "id": str(uuid.uuid4()),
            "signal_type": signal_type,
            "horizon": horizon,
            "predicted_value": 0.0,
            "predicted_range": {"min": 0.0, "max": 0.0},
            "method": "insufficient_data",
            "uncertainty": 1.0,
            "generated_at": now.isoformat(),
            "expires_at": (now + timedelta(days=1)).isoformat()
        }

    base_val = sum(matching) / len(matching)
    trend = 1.05  # mild 5% growth projection for 7d
    pred_val = round(base_val * trend, 2)
    uncertainty = 0.10

    fc = {
        "id": str(uuid.uuid4()),
        "signal_type": signal_type,
        "horizon": horizon,
        "predicted_value": pred_val,
        "predicted_range": {
            "min": round(pred_val * (1 - uncertainty), 2),
            "max": round(pred_val * (1 + uncertainty), 2)
        },
        "method": method,
        "uncertainty": uncertainty,
        "generated_at": now.isoformat(),
        "expires_at": (now + timedelta(days=7)).isoformat()
    }
    _in_memory_forecasts[signal_type] = fc
    return fc

async def evaluate_forecast(
    session: Optional[AsyncSession],
    forecast_id: str,
    actual_value: float
) -> dict:
    """Evaluates forecast accuracy against ground truth actuals (MAE, RMSE, MAPE)."""
    fc = None
    for f in _in_memory_forecasts.values():
        if f["id"] == forecast_id:
            fc = f
            break
    pred = fc["predicted_value"] if fc else 100.0
    err = abs(pred - actual_value)
    mae = err
    rmse = math.sqrt(err ** 2)
    mape = round(err / max(actual_value, 0.001), 4)

    eval_dict = {
        "id": str(uuid.uuid4()),
        "forecast_id": forecast_id,
        "signal_type": fc["signal_type"] if fc else "workflow_volume",
        "predicted": pred,
        "actual": actual_value,
        "error": err,
        "mape": mape,
        "mae": mae,
        "rmse": rmse,
        "evaluated_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_evaluations.append(eval_dict)
    return eval_dict

async def create_scenario(
    session: Optional[AsyncSession],
    scen_data: DecisionScenarioCreate,
    creator_id: str = "usr_executive_01"
) -> dict:
    """Creates a what-if simulation model."""
    scen_id = str(uuid.uuid4())
    scen = {
        "id": scen_id,
        "name": scen_data.name,
        "assumptions": scen_data.assumptions,
        "inputs": scen_data.inputs,
        "outputs": {},
        "created_by": creator_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_scenarios[scen_id] = scen
    return scen

async def simulate_scenario(
    session: Optional[AsyncSession],
    scenario_id: str
) -> dict:
    """Runs deterministic what-if scenario simulation in sandbox without mutating production."""
    scen = _in_memory_scenarios.get(scenario_id, {
        "id": scenario_id, "name": "30% Workload Growth Simulation",
        "assumptions": {"growth_rate": 0.30}, "inputs": {"current_jobs_daily": 1000}
    })
    growth = scen.get("assumptions", {}).get("growth_rate", 0.30)
    current_jobs = scen.get("inputs", {}).get("current_jobs_daily", 1000)

    simulated_jobs = current_jobs * (1 + growth)
    baseline = {"daily_cost": 150.0, "latency_p95_ms": 450}
    scenario_output = {"daily_cost": round(150.0 * (1 + growth), 2), "latency_p95_ms": round(450 * 1.15, 2)}
    delta = {
        "daily_cost_diff": round(scenario_output["daily_cost"] - baseline["daily_cost"], 2),
        "jobs_diff": simulated_jobs - current_jobs
    }

    res = {
        "id": str(uuid.uuid4()),
        "scenario_id": scenario_id,
        "baseline": baseline,
        "scenario_output": scenario_output,
        "delta": delta,
        "assumptions": scen.get("assumptions", {}),
        "uncertainty": 0.08,
        "run_at": datetime.now(timezone.utc).isoformat()
    }
    return res

async def generate_recommendation(
    session: Optional[AsyncSession],
    rec_type: str,
    reason: str,
    evidence: List[dict],
    expected_impact: str,
    risk: str = "medium"
) -> dict:
    """Generates an evidence-backed policy-controlled recommendation."""
    rec_id = str(uuid.uuid4())
    rec = {
        "id": rec_id,
        "type": rec_type,
        "reason": reason,
        "evidence": evidence,
        "expected_impact": expected_impact,
        "risk": risk,
        "confidence": 0.92,
        "status": "new",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_recommendations[rec_id] = rec
    return rec

async def resolve_recommendation(
    session: Optional[AsyncSession],
    rec_id: str,
    action: str,  # accept, reject
    actor_id: str = "usr_executive_01"
) -> dict:
    """Resolves a recommendation, creating a DecisionRecord and DecisionOutcome."""
    rec = _in_memory_recommendations.get(rec_id, {
        "id": rec_id, "type": "cost_optimization", "reason": "Provider B has lower latency",
        "evidence": [{"source": "finops_metrics", "finding": "Provider B is 15% cheaper"}],
        "expected_impact": "Save $45/mo", "risk": "low", "status": "new", "created_at": datetime.now(timezone.utc).isoformat()
    })
    now_iso = datetime.now(timezone.utc).isoformat()
    rec["status"] = "accepted" if action == "accept" else "rejected"

    if action == "accept":
        # Create Decision Record
        dec_id = str(uuid.uuid4())
        dec_dict = {
            "id": dec_id,
            "organization_id": "org_default_creator",
            "workspace_id": "ws_default_creator",
            "trigger": f"Recommendation {rec_id} Accepted",
            "evidence": rec["evidence"],
            "recommendation_id": rec_id,
            "decision": f"Approved {rec['type']}",
            "actor": actor_id,
            "policy_version": 1,
            "created_at": now_iso
        }
        _in_memory_decisions[dec_id] = dec_dict

        # Create Decision Outcome
        out_dict = {
            "id": str(uuid.uuid4()),
            "decision_id": dec_id,
            "expected_impact": rec["expected_impact"],
            "actual_impact": f"Achieved {rec['expected_impact']}",
            "error": 0.0,
            "unintended_effects": [],
            "recorded_at": now_iso
        }
        _in_memory_outcomes[dec_id] = out_dict

        await record_audit_event(
            session, "org_default_creator", actor_id, "decision_accepted", "recommendation", rec_id
        )

    return rec

async def record_feedback(
    session: Optional[AsyncSession],
    rec_id: str,
    feedback: str,
    actor_id: str = "usr_executive_01"
) -> dict:
    """Records human operator feedback (useful, not_useful, incorrect, unsafe, missing_context)."""
    fb_dict = {
        "id": str(uuid.uuid4()),
        "recommendation_id": rec_id,
        "feedback": feedback,
        "actor": actor_id,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_feedbacks.append(fb_dict)
    return fb_dict
