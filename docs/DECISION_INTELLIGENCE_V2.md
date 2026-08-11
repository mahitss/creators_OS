# Enterprise Decision Intelligence 2.0 & Evidence-Backed Decision Engine

Vapor OS Decision Intelligence 2.0 provides a governed decision engine that transforms objectives, context, evidence, options, constraints, risks, trade-offs, decisions, approvals, actions, outcomes, and evaluations.

## System Architecture

```
OBJECTIVE
    ↓
CONTEXT
    ↓
EVIDENCE (TrustedContextBuilder)
    ↓
OPTIONS (DecisionOptions)
    ↓
CONSTRAINTS
    ↓
RISK (Multi-Dimensional Matrix)
    ↓
TRADE-OFFS (DecisionTradeoff)
    ↓
DECISION
    ↓
APPROVAL (Human Override Audit)
    ↓
ACTION (ActionGateway)
    ↓
OUTCOME (Actual vs Expected)
    ↓
EVALUATION (Confidence Calibration)
```

> [!IMPORTANT]
> **Claim Classification Safeguard**:
> The system strictly distinguishes `FACT` (requires verified source evidence), `INFERENCE` (derived from evidence), `ASSUMPTION` (explicit assumption), `CONSTRAINT`, `PREDICTION` (time horizon, uncertainty), and `RECOMMENDATION` (reasoning summary, options considered, criteria). AI-generated recommendations are NEVER presented as authoritative facts.

## Core Directives
1. **Contradictory Evidence Preservation**: If sources conflict, both claims are preserved in `EvidenceConflict` with source authority ratings instead of silently picking a winner.
2. **Insufficient Information**: If evidence is lacking, returns `insufficient_information` instead of forcing an assumption-based recommendation.
3. **Immutable Versions & Human Overrides**: Material changes create a new `DecisionVersion`. Human overrides preserve original AI recommendations in the audit trail.
4. **Non-Destructive Scenario Simulator**: Executes "what-if" simulations without mutating production state.
