import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service, execution_governance_service

_in_memory_kpis: Dict[str, dict] = {}
_in_memory_targets: Dict[str, dict] = {}
_in_memory_measurements: Dict[str, dict] = {}
_in_memory_variances: Dict[str, dict] = {}
_in_memory_alerts: Dict[str, dict] = {}
_in_memory_drivers: Dict[str, dict] = {}
_in_memory_forecasts: Dict[str, dict] = {}
_in_memory_scorecards: Dict[str, dict] = {}

def _initialize_seed_performance_data():
    if _in_memory_kpis:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed KPI
    k1 = {
        "id": "kpi_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Security Threat Remediation Latency",
        "description": "Average duration from threat detection to active mitigation across all agent nodes.",
        "definition": "SUM(remediation_duration_seconds) / COUNT(resolved_threat_events)",
        "owner": "usr_secops_lead",
        "status": "active",
        "category": "security",
        "unit": "seconds",
        "direction": "lower_is_better",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_kpis[k1["id"]] = k1

    # Seed Target
    t1 = {
        "id": "tgt_01",
        "kpi_id": k1["id"],
        "target_value": 300.0, # 5 minutes
        "effective_from": "2026-07-01",
        "effective_to": "2026-12-31",
        "owner": "usr_exec_01",
        "approval_reference": "appr_sec_991",
        "version": 1
    }
    _in_memory_targets[t1["id"]] = t1

    # Seed Measurement
    m1 = {
        "id": "meas_01",
        "kpi_id": k1["id"],
        "value": 240.0, # 4 minutes
        "timestamp": now_iso,
        "period_start": "2026-08-01",
        "period_end": "2026-08-11",
        "source": "Vapor Event Mesh SIEM Sink",
        "quality": "verified",
        "confidence": 99.2
    }
    _in_memory_measurements[m1["id"]] = m1

    # Seed Variance
    v1 = {
        "id": "var_kpi_01",
        "kpi_id": k1["id"],
        "actual": 240.0,
        "target": 300.0,
        "baseline": 600.0,
        "delta": -60.0,
        "percentage_delta": -20.0,
        "severity": "low",
        "status": "on_track"
    }
    _in_memory_variances[v1["id"]] = v1

    # Seed Driver (Correlation - No unevidenced causality)
    d1 = {
        "id": "drv_01",
        "kpi_id": k1["id"],
        "driver_name": "Autonomous Agent Skill Upgrades (v2.4)",
        "driver_type": "operational",
        "association_type": "correlated",
        "confidence_pct": 89.5,
        "evidence_summary": "Strong statistical association between skill deployment and reduced response latency."
    }
    _in_memory_drivers[d1["id"]] = d1

    # Seed Forecast
    f1 = {
        "id": "fc_kpi_01",
        "kpi_id": k1["id"],
        "forecast_value": 210.0,
        "lower_bound": 180.0,
        "upper_bound": 250.0,
        "confidence_pct": 92.0,
        "generated_at": now_iso
    }
    _in_memory_forecasts[f1["id"]] = f1

    # Seed Scorecard
    s1 = {
        "id": "sc_01",
        "organization_id": org_id,
        "name": "Enterprise Security & Resilience Scorecard",
        "scorecard_type": "strategy",
        "kpi_ids_json": [k1["id"]]
    }
    _in_memory_scorecards[s1["id"]] = s1

_initialize_seed_performance_data()


class PerformanceIntelligenceService:

    @staticmethod
    async def get_performance_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_performance_data()
        kpis = list(_in_memory_kpis.values())
        targets = list(_in_memory_targets.values())
        measurements = list(_in_memory_measurements.values())
        variances = list(_in_memory_variances.values())
        alerts = list(_in_memory_alerts.values())
        drivers = list(_in_memory_drivers.values())
        forecasts = list(_in_memory_forecasts.values())
        scorecards = list(_in_memory_scorecards.values())

        on_track_count = sum(1 for v in variances if v["status"] == "on_track")
        on_track_rate = (on_track_count / len(variances)) * 100.0 if variances else 100.0

        return {
            "kpisCount": len(kpis),
            "onTrackRatePct": round(on_track_rate, 1),
            "staleCount": 0,
            "alertsCount": len(alerts),
            "scorecardsCount": len(scorecards),
            "kpis": kpis,
            "targets": targets,
            "measurements": measurements,
            "variances": variances,
            "alerts": alerts,
            "drivers": drivers,
            "forecasts": forecasts,
            "scorecards": scorecards,
            "performanceHealthScore": 0.95
        }

    @staticmethod
    async def create_kpi(session: Optional[AsyncSession], kpi_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_performance_data()
        k_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        k = {
            "id": k_id,
            "organization_id": org_id,
            "workspace_id": kpi_data.get("workspaceId", "ws_default"),
            "name": kpi_data["name"],
            "description": kpi_data["description"],
            "definition": kpi_data["definition"],
            "owner": kpi_data["owner"],
            "status": "active",
            "category": kpi_data.get("category", "operational"),
            "unit": kpi_data.get("unit", "USD"),
            "direction": kpi_data.get("direction", "higher_is_better"),
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_kpis[k_id] = k
        return k

    @staticmethod
    async def process_natural_language_performance_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_performance_data()

        # Enforce DLP checks on natural language query
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
                    "kpi_name": "Security Threat Remediation Latency",
                    "category": "security",
                    "status": "on_track",
                    "actual": "240 seconds",
                    "target": "300 seconds",
                    "trend": "improving",
                    "associated_driver": "Autonomous Agent Skill Upgrades (v2.4)"
                }
            ],
            "evidenceJson": {
                "referenced_kpis": ["kpi_01"],
                "referenced_measurements": ["meas_01"],
                "data_source": "KPI Operating System 2.0"
            },
            "confidencePct": 95.0
        }
