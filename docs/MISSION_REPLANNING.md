# Event-Driven Mission Replanning & Plan Versioning

Vapor OS supports adaptive, event-driven replanning while enforcing strict version control and safety limits.

## Replanning Triggers
- Dependency failure or resource unavailability.
- External condition or objective changes.
- Increasing deadline risk or budget variance.
- New evidence contradicting initial assumptions.

## Safety & Versioning Rules
- **Immutable Snapshots**: Every replan creates a new `MissionPlanVersion`. Active plans are never overwritten in-place.
- **Replan Diffs**: Replan requests generate structured diffs detailing added/removed steps and modified assignments.
- **Max Replans Limit**: `max_replans` prevents infinite replanning loops.
