# Policy-Governed Capability Discovery

`CapabilityDiscoveryService` handles search and discovery across enterprise capabilities.

## Access Status Resolution
Discovery responses return explicit access indicators (`accessible`, `approval_required`, `not_invokable`) based on PolicyEngine rules without exposing internal secret credentials.
