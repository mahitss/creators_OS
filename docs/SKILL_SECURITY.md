# Skill Security & Runtime Isolation

`invokeSkill()` enforces strict security boundaries on every invocation.

## Guardrails
- **ModelGateway**: Model calls route through ModelGateway capability resolution. Direct provider access is forbidden.
- **ActionGateway**: Tool calls route through ActionGateway enforcing identity, PolicyEngine, and DLP classification ceiling.
- **Side-Effect Contract**: Classifies actions as `read-only`, `external_mutation`, `communication`, `data_modification`, or `destructive`. High-risk contracts require explicit human approval.
- **Recursion & Depth Limits**: Circular call stacks (`skill A -> skill B -> skill A`) and depth exceeding `maxSkillDepth` are rejected.
