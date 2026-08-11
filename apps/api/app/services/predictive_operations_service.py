import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, performance_intelligence_service

_in_memory_forecasts: Dict[str, dict] = {}
_in_memory_forecast_points: Dict[str, dict] = {}
_in_memory_forecast_inputs: Dict[str, dict] = {}
_in_memory_forecast_drivers: Dict[str, dict] = {}
_in_memory_alerts: Dict[str, dict] = {}
_in_memory_risks: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_capacity_forecasts: Dict[str, dict] = {}
_in_memory_scenarios: Dict[str, dict] = {}
_in_memory_accuracies: Dict[str, dict] = {}

def _initialize_seed_predictive_data():
    if _in_memory_forecasts:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Forecast
    f1 = {
        "id": "fc_v2_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "entity_type": "kpi",
        "entity_id": "kpi_01",
        "metric_id": "metric_remediation_latency",
        "horizon": "medium_term",
        "method": "ensemble_timeseries_v2",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_forecasts[f1["id"]] = f1

    # Seed Forecast Point
    fp1 = {
        "id": "fp_01",
        "forecast_id": f1["id"],
        "timestamp": now_iso,
        "value": 210.0,
        "lower_bound": 185.0,
        "upper_bound": 240.0,
        "confidence": 92.5
    }
    _in_memory_forecast_points[fp1["id"]] = fp1

    # Seed Forecast Input
    fi1 = {
        "id": "fi_01",
        "forecast_id": f1["id"],
        "input_type": "historical_series",
        "source_name": "Vapor Performance Intelligence Engine (30-day window)",
        "quality": "verified"
    }
    _in_memory_forecast_inputs[fi1["id"]] = fi1

    # Seed Forecast Driver (Associated with language)
    fd1 = {
        "id": "fdr_01",
        "forecast_id": f1["id"],
        "factor_name": "Agent Subsystem Memory Allocation Optimization",
        "direction": "positive",
        "magnitude": 0.35,
        "evidence": "Observed 18% reduction in latency following memory heap tuning.",
        "confidence_pct": 89.0,
        "association_type": "correlated"
    }
    _in_memory_forecast_drivers[fd1["id"]] = fd1

    # Seed Predictive Alert (Window range e.g. "Likely within 14-21 days")
    pa1 = {
        "id": "pa_01",
        "forecast_id": f1["id"],
        "alert_type": "deadline_miss",
        "predicted_window": "Likely within 14-21 days",
        "confidence": "high",
        "status": "open",
        "created_at": now_iso
    }
    _in_memory_alerts[pa1["id"]] = pa1

    # Seed Predictive Risk Signal (Probability range e.g. "60-75%")
    pr1 = {
        "id": "pr_01",
        "forecast_id": f1["id"],
        "risk_id": "risk_sec_latency_spike",
        "affected_entity_id": "initiative_sec_01",
        "probability_range": "60-75%",
        "impact": "high",
        "evidence": "Telemetry indicates potential memory saturation under peak agent loads."
    }
    _in_memory_risks[pr1["id"]] = pr1

    # Seed Predictive Recommendation (Advisory)
    rec1 = {
        "id": "rec_01",
        "signal_id": pr1["id"],
        "options_json": [
            {"option": "Increase Agent Node Replica Pool", "effect": "Reduces peak latency by 30%"},
            {"option": "Enable Adaptive Task Throttling", "effect": "Prevents memory spillover"}
        ],
        "expected_effect": "Mitigates high-load latency risk before milestone deadline.",
        "risk_level": "medium",
        "confidence_pct": 91.0,
        "status": "advisory"
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    # Seed Capacity Forecast
    cf1 = {
        "id": "cap_fc_01",
        "capacity_type": "agent",
        "demand_value": 450.0,
        "capacity_value": 400.0,
        "gap": 50.0, # Gap of 50 agent execution threads
        "horizon": "medium_term"
    }
    _in_memory_capacity_forecasts[cf1["id"]] = cf1

    # Seed Forecast Scenario
    fs1 = {
        "id": "fsc_01",
        "forecast_id": f1["id"],
        "scenario_name": "downside",
        "scenario_params_json": {"capacity_drop_pct": 15.0},
        "output_distribution_json": {"expected_latency_p99": 310.0, "risk_increase": "moderate"}
    }
    _in_memory_scenarios[fs1["id"]] = fs1

    # Seed Forecast Accuracy
    fa1 = {
        "id": "fa_01",
        "forecast_id": f1["id"],
        "actual_value": 215.0,
        "absolute_error": 5.0,
        "percentage_error": 2.38,
        "interval_coverage": 96.0,
        "calibration": 94.0
    }
    _in_memory_accuracies[fa1["id"]] = fa1

_initialize_seed_predictive_data()


class PredictiveOperationsService:

    @staticmethod
    async def get_predictions_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_predictive_data()
        forecasts = list(_in_memory_forecasts.values())
        points = list(_in_memory_forecast_points.values())
        alerts = list(_in_memory_alerts.values())
        risks = list(_in_memory_risks.values())
        recommendations = list(_in_memory_recommendations.values())
        capacity = list(_in_memory_capacity_forecasts.values())
        scenarios = list(_in_memory_scenarios.values())
        accuracies = list(_in_memory_accuracies.values())

        return {
            "forecastsCount": len(forecasts),
            "alertsCount": len(alerts),
            "risksCount": len(risks),
            "capacityGapsCount": sum(1 for c in capacity if c["gap"] > 0),
            "forecasts": forecasts,
            "points": points,
            "alerts": alerts,
            "risks": risks,
            "recommendations": recommendations,
            "capacityForecasts": capacity,
            "scenarios": scenarios,
            "accuracies": accuracies,
            "overallAccuracyPct": 95.8,
            "predictionHealthScore": 0.94
        }

    @staticmethod
    async def create_forecast(session: Optional[AsyncSession], fc_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_predictive_data()
        fc_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        fc = {
            "id": fc_id,
            "organization_id": org_id,
            "workspace_id": fc_data.get("workspaceId", "ws_default"),
            "entity_type": fc_data.get("entityType", "kpi"),
            "entity_id": fc_data["entityId"],
            "metric_id": fc_data.get("metricId"),
            "horizon": fc_data.get("horizon", "medium_term"),
            "method": fc_data.get("method", "ensemble_timeseries"),
            "status": "active",
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_forecasts[fc_id] = fc
        return fc

    @staticmethod
    async def process_natural_language_predictive_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_predictive_data()

        # Enforce DLP checks on natural language query
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Privacy Anti-Surveillance Safeguard (No employee performance / termination predictions)
        lower_q = query_str.lower()
        if any(p in lower_q for p in ["fire", "terminate", "employee", "worker", "promotion", "ranking"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Denied. Employee surveillance or individual performance prediction is strictly prohibited by policy."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "forecast_entity": "kpi_01 (Security Threat Remediation Latency)",
                    "predicted_value": "210 seconds",
                    "predicted_window": "Likely within 14-21 days",
                    "confidence_pct": "92.5%",
                    "associated_driver": "Agent Subsystem Memory Allocation Optimization"
                }
            ],
            "evidenceJson": {
                "referenced_forecasts": ["fc_v2_01"],
                "data_source": "Predictive Operations 2.0 Engine"
            },
            "confidencePct": 92.5
        }
