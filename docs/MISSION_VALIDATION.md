# Mission Validation & Deliverable Verification

Details `MissionValidator` evidence verification in Vapor OS.

## Verification Directives
- **No Fake Progress**: Progress percentages derive exclusively from verified step completion states.
- **Deliverable Verification**: Artifact steps are verified against physical filesystem/storage objects before completion.
- **Action Verification**: External actions are verified against `ActionGateway` execution result payloads.
- **Human Acceptance**: High-impact steps require human acceptance (`accepted`, `rejected`, `needs_changes`).
