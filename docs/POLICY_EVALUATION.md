# Policy Evaluation Pipeline

Details the evaluation pipeline in Vapor OS Policy Intelligence 2.0.

## Evaluation Pipeline Steps
1. **Request Normalization**: Normalizes action (`read`, `write`, `delete`, `send`, `execute`, `approve`, `deploy`, `publish`, `export`, `share`) and resource (`document`, `email`, `calendar`, `database`, `API`, `tool`, `workflow`, `agent`, `skill`, `capability`, `model`, `knowledge_object`).
2. **Risk Scoring**: Evaluates 7 dimensions (`data`, `financial`, `security`, `privacy`, `operational`, `compliance`, `reputational`). Note: Risk informs policy, risk != permission.
3. **Precedence Matching**: Applies hierarchy (Organization > Workspace > Team > Agent > Mission > Capability).
4. **Control Chains**: Executes required controls (e.g. DLP redaction, dual approval).
5. **Fail-Closed Safeguard**: Strict default `DENY` if evaluation fails or policy service is unavailable.
