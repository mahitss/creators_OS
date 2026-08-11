# Incident Response & Correlation Architecture

Vapor OS Security Fabric correlates related security events into unified incidents and threat chains.

## Incident Lifecycle
1. **Detect**: Security signals ingested from runtime & scanners.
2. **Triage**: Classified by severity (`info`, `low`, `medium`, `high`, `critical`).
3. **Contain**: Automated or manual quarantine of affected agents/capabilities.
4. **Investigate**: Attack chain graph analysis & evidence verification.
5. **Recover**: Security review and authorized quarantine release.
6. **Close**: Audit log updated.
