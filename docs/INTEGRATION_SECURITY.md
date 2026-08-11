# Integration Security & Network Boundaries

## SSRF Protection & Network Isolation
- **SSRF Rules**: External destinations are validated before execution. Rejects private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `localhost`) and cloud metadata endpoints (`169.254.169.254`).
- **PolicyEngine & DLP**: Every external write passes through PolicyEngine resource authorization and DLP boundary evaluation.
