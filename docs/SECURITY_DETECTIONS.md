# Threat Detection Rule Lifecycle & Shadow Mode

Threat detection rules monitor runtime events for prompt injection, tool abuse, exfiltration, and privilege escalation.

## Rule Lifecycle
`draft -> simulation -> shadow -> active -> paused -> deprecated`

## Shadow Mode
Rules in `shadow` mode emit telemetry signals and track false-positive rates without triggering production response actions or agent quarantine.
