from typing import Dict, Any, List

EVALUATION_DATASET: List[dict] = [
    {
        "id": "eval_mp_01",
        "operation": "mission_planning",
        "input": {"title": "Build Docker Container", "description": "Package FastAPI app into Docker image."},
        "expected_fields": ["goal", "summary", "steps", "deliverables"],
        "min_steps": 2
    },
    {
        "id": "eval_eb_01",
        "operation": "executive_brief",
        "input": {"user_name": "Alex", "needs_attention_count": 1, "active_missions_count": 2},
        "expected_fields": ["summary_statement", "needs_attention", "primary_recommendation"],
        "forbidden_phrases": ["0%", "0 tasks"]
    },
    {
        "id": "eval_cg_01",
        "operation": "content_generation",
        "input": {"type": "article", "title": "Docker Setup Guide"},
        "expected_fields": ["title", "content"],
        "min_length": 50
    },
    {
        "id": "eval_me_01",
        "operation": "memory_extraction",
        "input": {"mission_title": "Build Docker Container"},
        "expected_fields": ["title", "content", "type"],
        "valid_types": ["preference", "fact", "decision", "goal", "insight", "lesson"]
    },
    {
        "id": "eval_da_01",
        "operation": "deliverable_analysis",
        "input": {"mission_title": "Research Competitor Docker Adoption"},
        "expected_fields": ["type", "title", "reason"],
        "valid_types": ["article", "script", "social_post", "email", "report", "outline"]
    }
]

def evaluate_ai_output(operation: str, output: Dict[str, Any]) -> Dict[str, Any]:
    test_cases = [tc for tc in EVALUATION_DATASET if tc["operation"] == operation]
    if not test_cases:
        return {"passed": True, "cases_evaluated": 0, "score": 1.0}

    passed_count = 0
    failures = []

    for tc in test_cases:
        case_passed = True
        for field in tc.get("expected_fields", []):
            if field not in output or output[field] is None:
                case_passed = False
                failures.append(f"Case {tc['id']}: Missing expected field '{field}'")

        if "min_steps" in tc and isinstance(output.get("steps"), list):
            if len(output["steps"]) < tc["min_steps"]:
                case_passed = False
                failures.append(f"Case {tc['id']}: Expected at least {tc['min_steps']} steps.")

        if "min_length" in tc and isinstance(output.get("content"), str):
            if len(output["content"]) < tc["min_length"]:
                case_passed = False
                failures.append(f"Case {tc['id']}: Output length less than {tc['min_length']} characters.")

        if case_passed:
            passed_count += 1

    total = len(test_cases)
    return {
        "operation": operation,
        "passed": passed_count == total,
        "cases_evaluated": total,
        "passed_count": passed_count,
        "score": round(passed_count / total, 2),
        "failures": failures
    }
