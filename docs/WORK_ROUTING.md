# Policy-Governed Work Routing Architecture

`WorkRouter` selects human, agent, or hybrid execution using capability, availability, authorization, risk, deadline, cost, workload fairness, and verified expertise profiles (`ExpertiseProfile`).

## Work Classification Types
- `automatable`: Repetitive task candidate for automated execution.
- `agent_suitable`: Autonomous execution by authorized agents.
- `human_required`: Requires human judgment, policy exception, or high-impact sign-off.
- `hybrid`: Collaborative execution combining agent synthesis with human review.
- `restricted`: High-security task constrained by data policies.
