import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import model_gateway_service

_in_memory_components: Dict[str, dict] = {}
_in_memory_failures: List[dict] = []
_in_memory_degradations: Dict[str, dict] = {}
_in_memory_circuits: Dict[str, dict] = {}
_in_memory_dead_letters: Dict[str, dict] = {}
_in_memory_recovery_plans: Dict[str, dict] = {}
_in_memory_experiments: Dict[str, dict] = {}
_in_memory_slos: Dict[str, dict] = {}
_in_memory_budgets: Dict[str, dict] = {}
_in_memory_leases: Dict[str, dict] = {}
_in_memory_idempotency_keys: Dict[str, dict] = {}

def _initialize_demo_resilience_data():
    if _in_memory_components:
        return
    now_iso = datetime.now(timezone.utc).isoformat()

    # Components
    comps = [
        {"id": "comp_agent_runtime", "component_id": "agent_runtime_v2", "component_type": "agent", "status": "healthy", "latency_ms": 42.0, "error_rate": 0.001, "availability_pct": 99.98, "last_healthy_at": now_iso, "updated_at": now_iso},
        {"id": "comp_model_gateway", "component_id": "model_gateway", "component_type": "model", "status": "healthy", "latency_ms": 180.0, "error_rate": 0.002, "availability_pct": 99.95, "last_healthy_at": now_iso, "updated_at": now_iso},
        {"id": "comp_gmail_integration", "component_id": "gmail_integration", "component_type": "integration", "status": "degraded", "latency_ms": 1250.0, "error_rate": 0.05, "availability_pct": 95.0, "last_healthy_at": now_iso, "updated_at": now_iso},
        {"id": "comp_event_mesh", "component_id": "event_mesh", "component_type": "event_stream", "status": "healthy", "latency_ms": 12.0, "error_rate": 0.0001, "availability_pct": 99.99, "last_healthy_at": now_iso, "updated_at": now_iso},
        {"id": "comp_database", "component_id": "primary_postgres", "component_type": "database", "status": "healthy", "latency_ms": 5.0, "error_rate": 0.0, "availability_pct": 99.999, "last_healthy_at": now_iso, "updated_at": now_iso}
    ]
    for c in comps:
        _in_memory_components[c["component_id"]] = c

    # Degradation
    deg_id = "deg_demo_01"
    _in_memory_degradations[deg_id] = {
        "id": deg_id,
        "scope": "integration:gmail",
        "mode": "approval_required",
        "reason": "Gmail API rate limit elevation; requiring human confirmation for external messages",
        "status": "active",
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
        "created_at": now_iso
    }

    # Circuit Breakers
    _in_memory_circuits["gmail_api"] = {
        "id": "cb_gmail",
        "target_name": "gmail_api",
        "state": "half_open",
        "failure_count": 3,
        "last_state_change_at": now_iso
    }

    # Recovery Plan
    rp_id = "rp_dr_regional_01"
    _in_memory_recovery_plans[rp_id] = {
        "id": rp_id,
        "name": "Primary Region Failover & State Reconstruction Plan",
        "components_json": ["database", "event_mesh", "agent_runtime_v2"],
        "rto_seconds": 300,
        "rpo_seconds": 60,
        "recovery_order_json": ["1. Re-establish Database Read Replicas", "2. Reconstruct Agent Runtime Checkpoints", "3. Replay Event Mesh Outbox"],
        "status": "active",
        "created_at": now_iso
    }

    # Chaos Experiment
    exp_id = "exp_latency_inj_01"
    _in_memory_experiments[exp_id] = {
        "id": exp_id,
        "name": "Model Provider Latency Spike Simulation",
        "experiment_type": "latency_injection",
        "target_scope": "sandbox_workspace",
        "blast_radius_json": {"max_affected_missions": 5, "allow_production": False},
        "abort_conditions_json": {"max_error_rate": 0.05, "max_latency_ms": 3000.0},
        "status": "draft",
        "created_at": now_iso
    }

    # SLOs
    _in_memory_slos["slo_mission_exec"] = {
        "id": "slo_mission_exec",
        "slo_name": "Mission Execution Availability",
        "target_availability_pct": 99.9,
        "current_availability_pct": 99.95,
        "target_latency_ms": 250.0,
        "current_latency_ms": 42.0,
        "status": "compliant",
        "updated_at": now_iso
    }

    # Budget
    _in_memory_budgets["org_default_creator"] = {
        "id": "bgt_default",
        "organization_id": "org_default_creator",
        "allowed_error_pct": 0.1,
        "current_burn_rate": 0.015,
        "budget_remaining_pct": 85.0,
        "updated_at": now_iso
    }

_initialize_demo_resilience_data()


class ResilienceService:

    @staticmethod
    async def get_dashboard_summary(session: Optional[AsyncSession]) -> dict:
        _initialize_demo_resilience_data()
        comps = list(_in_memory_components.values())
        degs = [d for d in _in_memory_degradations.values() if d.get("status") == "active"]
        open_cbs = [c for c in _in_memory_circuits.values() if c.get("state") in ["open", "half_open"]]
        active_exps = [e for e in _in_memory_experiments.values() if e.get("status") == "running"]
        slos = list(_in_memory_slos.values())

        unhealthy_count = len([c for c in comps if c.get("status") in ["unavailable", "degraded"]])
        overall_status = "healthy"
        if unhealthy_count > 0:
            overall_status = "degraded"

        return {
            "overallStatus": overall_status,
            "totalComponentsCount": len(comps),
            "unhealthyComponentsCount": unhealthy_count,
            "activeDegradationModesCount": len(degs),
            "openCircuitBreakersCount": len(open_cbs),
            "activeExperimentsCount": len(active_exps),
            "deadLetterCount": len(_in_memory_dead_letters),
            "components": comps,
            "degradations": degs,
            "circuits": list(_in_memory_circuits.values()),
            "slos": slos,
            "capacity": {
                "cpuPct": 38.5,
                "memoryPct": 44.0,
                "queueDepth": 8,
                "concurrencyLevel": 12,
                "loadSheddingActive": False
            }
        }

    @staticmethod
    async def classify_failure(session: Optional[AsyncSession], component_id: str, failure_type: str, evidence: dict) -> dict:
        _initialize_demo_resilience_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        ev_id = str(uuid.uuid4())

        failure_rec = {
            "id": ev_id,
            "component_id": component_id,
            "failure_type": failure_type,
            "evidence_json": evidence,
            "created_at": now_iso
        }
        _in_memory_failures.append(failure_rec)

        # Update component status
        if component_id in _in_memory_components:
            _in_memory_components[component_id]["status"] = "degraded"
            _in_memory_components[component_id]["updated_at"] = now_iso

        return failure_rec

    @staticmethod
    async def evaluate_model_fallback(session: Optional[AsyncSession], requested_provider: str, model_id: str, is_restricted_data: bool) -> dict:
        _initialize_demo_resilience_data()
        models = await model_gateway_service.list_models(session)
        compliant = [m for m in models if m.get("status") == "available"]
        if is_restricted_data:
            compliant = [m for m in compliant if m.get("provider_id") == "google"]

        if not compliant:
            return {
                "status": "failed_safely",
                "reason": "No compliant model provider available under active DLP policy",
                "security_controls_active": True
            }
        return {
            "status": "fallback_selected",
            "fallback": compliant[0],
            "security_controls_active": True
        }

    @staticmethod
    async def acquire_state_lease(session: Optional[AsyncSession], resource_id: str, worker_id: str, ttl_seconds: int = 30) -> dict:
        _initialize_demo_resilience_data()
        now = datetime.now(timezone.utc)
        existing = _in_memory_leases.get(resource_id)

        if existing and existing["status"] == "active":
            exp_time = datetime.fromisoformat(existing["expires_at"])
            if exp_time > now and existing["owner_worker_id"] != worker_id:
                return {
                    "status": "denied",
                    "reason": f"Split-brain protection: Resource '{resource_id}' leased by worker '{existing['owner_worker_id']}' until {existing['expires_at']}"
                }

        expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat()
        lease = {
            "id": str(uuid.uuid4()),
            "resource_id": resource_id,
            "owner_worker_id": worker_id,
            "starts_at": now.isoformat(),
            "expires_at": expires_at,
            "status": "active"
        }
        _in_memory_leases[resource_id] = lease
        return {"status": "acquired", "lease": lease}

    @staticmethod
    async def reconcile_external_action(session: Optional[AsyncSession], idempotency_key: str, action_type: str, action_payload: dict) -> dict:
        _initialize_demo_resilience_data()
        if idempotency_key in _in_memory_idempotency_keys:
            prev = _in_memory_idempotency_keys[idempotency_key]
            return {
                "reconciled": True,
                "duplicate_detected": True,
                "original_result": prev["result"],
                "execution_count": prev["count"]
            }

        result = {"status": "executed", "action": action_type, "timestamp": datetime.now(timezone.utc).isoformat()}
        _in_memory_idempotency_keys[idempotency_key] = {
            "result": result,
            "count": 1
        }
        return {"reconciled": True, "duplicate_detected": False, "result": result}

    @staticmethod
    async def check_circuit_breaker(session: Optional[AsyncSession], target_name: str) -> dict:
        _initialize_demo_resilience_data()
        cb = _in_memory_circuits.get(target_name)
        if not cb:
            cb = {
                "id": str(uuid.uuid4()),
                "target_name": target_name,
                "state": "closed",
                "failure_count": 0,
                "last_state_change_at": datetime.now(timezone.utc).isoformat()
            }
            _in_memory_circuits[target_name] = cb
        return cb

    @staticmethod
    async def trip_circuit_breaker(session: Optional[AsyncSession], target_name: str) -> dict:
        _initialize_demo_resilience_data()
        cb = await ResilienceService.check_circuit_breaker(session, target_name)
        cb["state"] = "open"
        cb["failure_count"] += 1
        cb["last_state_change_at"] = datetime.now(timezone.utc).isoformat()
        return cb

    @staticmethod
    async def push_dead_letter(session: Optional[AsyncSession], message_ref: str, queue_name: str, reason: str) -> dict:
        _initialize_demo_resilience_data()
        dl_id = str(uuid.uuid4())
        rec = {
            "id": dl_id,
            "message_ref": message_ref,
            "queue_name": queue_name,
            "failure_reason": reason,
            "attempts": 3,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_dead_letters[dl_id] = rec
        return rec

    @staticmethod
    async def replay_dead_letter(session: Optional[AsyncSession], dead_letter_id: str) -> dict:
        _initialize_demo_resilience_data()
        entry = _in_memory_dead_letters.get(dead_letter_id)
        if not entry:
            return {"error": f"Dead letter entry '{dead_letter_id}' not found"}
        entry["status"] = "replayed"
        return {"id": dead_letter_id, "status": "replayed", "replayed_at": datetime.now(timezone.utc).isoformat()}

    @staticmethod
    async def create_recovery_plan(session: Optional[AsyncSession], plan_data: dict) -> dict:
        _initialize_demo_resilience_data()
        rp_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        rec = {
            "id": rp_id,
            "name": plan_data.get("name", "Custom Recovery Plan"),
            "components_json": plan_data.get("componentsJson", []),
            "rto_seconds": plan_data.get("rtoSeconds", 300),
            "rpo_seconds": plan_data.get("rpoSeconds", 60),
            "recovery_order_json": plan_data.get("recoveryOrderJson", []),
            "status": "active",
            "created_at": now_iso
        }
        _in_memory_recovery_plans[rp_id] = rec
        return rec

    @staticmethod
    async def simulate_recovery_plan(session: Optional[AsyncSession], plan_id: str) -> dict:
        _initialize_demo_resilience_data()
        plan = _in_memory_recovery_plans.get(plan_id)
        if not plan:
            return {"error": f"Recovery plan '{plan_id}' not found"}

        return {
            "plan_id": plan_id,
            "simulation_result": "SUCCESS",
            "production_impact": "NONE (Dry Run)",
            "estimated_rto_seconds": plan["rto_seconds"],
            "estimated_rpo_seconds": plan["rpo_seconds"]
        }

    @staticmethod
    async def start_chaos_experiment(session: Optional[AsyncSession], experiment_id: str) -> dict:
        _initialize_demo_resilience_data()
        exp = _in_memory_experiments.get(experiment_id)
        if not exp:
            return {"error": f"Chaos experiment '{experiment_id}' not found"}

        exp["status"] = "running"
        return exp

    @staticmethod
    async def abort_chaos_experiment(session: Optional[AsyncSession], experiment_id: str, reason: str = "Blast radius threshold reached") -> dict:
        _initialize_demo_resilience_data()
        exp = _in_memory_experiments.get(experiment_id)
        if not exp:
            return {"error": f"Chaos experiment '{experiment_id}' not found"}

        exp["status"] = "aborted"
        return {"id": experiment_id, "status": "aborted", "abort_reason": reason}
