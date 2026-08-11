# Evaluation Datasets & Golden Suites

## Dataset Architecture
`EvaluationDataset` stores versioned evaluation case collections across initial types: `question_answer`, `retrieval`, `agent_task`, `workflow_task`, `decision`, `safety`, `tool_selection`, `citation`.

## Golden Datasets
Golden datasets represent curated ground-truth cases that require human owner review and version publishing. They adhere to tenant isolation, classification, and DLP sanitization.
