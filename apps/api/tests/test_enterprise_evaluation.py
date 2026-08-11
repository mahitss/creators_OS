import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import enterprise_evaluation_service
from app.schemas.enterprise_evaluation import (
    EvaluationRunCreate,
    EvaluationDatasetCreate,
    HumanEvaluationCreate,
    EvaluationExperimentCreate
)

def test_evaluation_dataset_creation_and_listing():
    async def _test():
        req = EvaluationDatasetCreate(
            name="Agent Tool Selection Benchmark",
            version="1.0",
            description="Test suite for tool call precision",
            isGolden=True
        )
        ds = await enterprise_evaluation_service.create_evaluation_dataset(None, workspace_id="ws_default_01", req=req)
        assert ds is not None
        assert ds["is_golden"] is True

        datasets = await enterprise_evaluation_service.list_evaluation_datasets(None, workspace_id="ws_default_01")
        assert len(datasets) >= 2
    asyncio.run(_test())

def test_evaluation_run_execution_and_results():
    async def _test():
        req = EvaluationRunCreate(
            evaluationType="benchmark",
            targetType="response",
            targetId="model_gemini_1_5_pro",
            model="gemini-1.5-pro",
            modelVersion="1.0",
            promptVersion="v1.0"
        )
        run = await enterprise_evaluation_service.create_evaluation_run(None, workspace_id="ws_default_01", req=req)
        assert run is not None
        assert run["status"] == "completed"

        results = await enterprise_evaluation_service.list_evaluation_results(None, run_id=run["id"])
        assert len(results) >= 5
        metrics = [r["metric"] for r in results]
        assert "groundedness" in metrics
        assert "safety" in metrics
    asyncio.run(_test())

def test_human_evaluation_submission_and_calibration():
    async def _test():
        req = HumanEvaluationCreate(
            caseId="case_01",
            evaluationRunId="run_baseline_01",
            criteria="groundedness",
            rating=5.0,
            comment="Fully supported by authoritative Google Drive document"
        )
        he = await enterprise_evaluation_service.submit_human_evaluation(None, evaluator_id="usr_executive_01", req=req)
        assert he["rating"] == 5.0

        reviews = await enterprise_evaluation_service.list_human_evaluations(None)
        assert len(reviews) >= 1
    asyncio.run(_test())

def test_experimentation_ab_testing():
    async def _test():
        req = EvaluationExperimentCreate(
            name="Prompt v1 vs v2 Grounding Comparison",
            baselineConfig={"promptVersion": "v1.0", "model": "gemini-1.5-pro"},
            candidateConfig={"promptVersion": "v2.0", "model": "gemini-1.5-pro"}
        )
        exp = await enterprise_evaluation_service.create_experiment(None, req=req)
        assert exp["status"] == "running"

        stopped = await enterprise_evaluation_service.stop_experiment(None, experiment_id=exp["id"])
        assert stopped["status"] == "stopped"
    asyncio.run(_test())

def test_evaluation_overview_telemetry():
    async def _test():
        ov = await enterprise_evaluation_service.get_evaluation_overview(None)
        assert ov["grounding_rate"] >= 0.90
        assert ov["citation_accuracy"] >= 0.90
        assert ov["judge_calibration_score"] >= 0.90
    asyncio.run(_test())
