# Vapor OS — AI Evaluation Framework

## 1. Overview
Vapor OS uses a deterministic, repeatable evaluation framework to test AI operation outputs against synthetic contract datasets before deployment.

## 2. Tested Operations
1. `mission_planning`: Validates step structure, goal alignment, and deliverable schemas.
2. `executive_brief`: Ensures facts are grounded and avoids hallucinated metrics.
3. `content_generation`: Verifies deliverable format and content length constraints.
4. `memory_extraction`: Validates preference and lesson insight candidate schemas.
5. `deliverable_analysis`: Checks classification confidence and reason grounding.

## 3. Evaluation Execution
Evaluations are run via Pytest (`pytest apps/api/tests/test_reliability.py`) and CI contract suites to prevent AI regressions.
