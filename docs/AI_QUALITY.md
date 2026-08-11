# AI Quality Dimensions & Telemetry

## Evaluation Dimensions
Vapor measures 11 distinct evaluation dimensions:
- `correctness`: Factual accuracy against ground truth or evidence.
- `relevance`: Alignment of response content with user request.
- `groundedness`: Claim support by retrieved evidence.
- `citation_accuracy`: Citation validity and source accessibility.
- `completeness`: Goal coverage and required field presence.
- `instruction_following`: Strict adherence to user constraints and policy.
- `tool_correctness`: Tool choice, argument schema, and resource scoping.
- `policy_compliance`: Compliance with central policy engine rules.
- `safety`: Freedom from prompt injection, exfiltration, or harmful instructions.
- `latency`: Execution response time.
- `cost`: Token cost and resource consumption.
