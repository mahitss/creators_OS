# Vapor OS — Human-in-the-Loop Approval System

## 1. Stale Approval & Input Hash Protection
Before executing an approved request, `agent_runtime` re-validates the tool input SHA-256 hash (`input_hash`). If parameters were altered before execution, the approval is invalidated (`APPROVAL_EXPIRED`).

## 2. Double Approval Idempotency
Atomic state transitions (`pending` $\rightarrow$ `approved` $\rightarrow$ `executing` $\rightarrow$ `completed`) ensure that repeated clicks on `Approve Action` execute external side-effect tools exactly once.

## 3. Provider Verification
External actions verify provider response payloads (e.g. Google Calendar event ID) before updating normalized local database records. Never claim success if external APIs fail.
