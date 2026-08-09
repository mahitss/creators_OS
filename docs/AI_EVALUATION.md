# Vapor OS — AI Evaluation Framework

## 1. Overview
Vapor OS uses a deterministic, repeatable evaluation framework to test AI operation outputs against synthetic contract datasets before deployment. In Sprint 24, this framework was extended into the Agent Evaluation + Simulation Lab.

## 2. Tested Operations & Categories
1. `mission_planning`: Validates step structure, goal alignment, DAG constraints, and deliverable schemas.
2. `executive_brief`: Ensures facts are grounded and avoids hallucinated metrics.
3. `content_generation`: Verifies deliverable format and content length constraints.
4. `memory_extraction`: Validates preference and lesson insight candidate schemas.
5. `deliverable_analysis`: Checks classification confidence and reason grounding.
6. `tool_selection` & `tool_arguments`: Validates accurate tool choice and structured parameter schemas.
7. `authorization` & `approval`: Enforces cross-workspace isolation and approval gates.
8. `prompt_injection` & `failure_recovery`: Tests prompt injection resistance and fault recovery.

## 3. Evaluation Execution & Release Gates
Evaluations are executed deterministically via `evaluation_runner.py` and Pytest suites (`test_evaluation_lab.py`, `test_eval_chaos.py`). Build deployment requires passing all release gate safety thresholds.
