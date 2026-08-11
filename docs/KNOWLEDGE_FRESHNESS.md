# Knowledge Freshness & Stale Object Tracking

## Freshness Policies
Vapor applies source-specific TTL policies rather than a single global TTL:
- Corporate Policies: 365 days
- Technical Specifications: 30 days
- Incident Status: 5 minutes (300 seconds)
- Integration Telemetry: 1 hour (3600 seconds)

## Stale Retrieval Behavior
Stale knowledge is tagged `stale` during retrieval. Vapor surfaces stale warnings rather than presenting outdated content as current fact.
