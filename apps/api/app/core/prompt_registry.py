from typing import Dict, Optional
from datetime import datetime, timezone

PROMPT_REGISTRY: Dict[str, dict] = {
    "mission_planning": {
        "prompt_id": "prompt_mission_plan_v1",
        "version": "1.0.0",
        "operation": "mission_planning",
        "active_flag": True,
        "template": "You are Executive AI for Vapor OS. Formulate structured mission execution steps, deliverables, and open questions.",
        "created_at": "2026-08-08T00:00:00Z"
    },
    "executive_brief": {
        "prompt_id": "prompt_exec_brief_v1",
        "version": "1.0.0",
        "operation": "executive_brief",
        "active_flag": True,
        "template": "Summarize provided workspace facts into a concise executive brief. Do not introduce non-existent facts.",
        "created_at": "2026-08-08T00:00:00Z"
    },
    "content_generation": {
        "prompt_id": "prompt_content_gen_v1",
        "version": "1.0.0",
        "operation": "content_generation",
        "active_flag": True,
        "template": "Refine or draft the deliverable text based on mission context and workspace memories.",
        "created_at": "2026-08-08T00:00:00Z"
    },
    "memory_extraction": {
        "prompt_id": "prompt_mem_extract_v1",
        "version": "1.0.0",
        "operation": "memory_extraction",
        "active_flag": True,
        "template": "Extract actionable workspace preferences, facts, or lessons learned from completed mission executions.",
        "created_at": "2026-08-08T00:00:00Z"
    },
    "deliverable_analysis": {
        "prompt_id": "prompt_deliv_analysis_v1",
        "version": "1.0.0",
        "operation": "deliverable_analysis",
        "active_flag": True,
        "template": "Analyze completed mission execution outputs and classify potential deliverable opportunities.",
        "created_at": "2026-08-08T00:00:00Z"
    }
}

def get_active_prompt(operation: str) -> Optional[dict]:
    prompt = PROMPT_REGISTRY.get(operation)
    if prompt and prompt["active_flag"]:
        return prompt
    return None
