# Threat Escalation Paths & Materialization Linkage

`ThreatEscalationPath` traces `Signal -> Risk -> Threat -> Incident -> Crisis` escalation paths with explicit condition checks.

When a threat materializes, Vapor links `EmergingThreat -> Incident -> Crisis` while preserving human crisis declaration governance (Sprint 70).
