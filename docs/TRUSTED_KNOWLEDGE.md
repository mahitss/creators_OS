# Trusted Knowledge & Context Building

## TrustedContextBuilder
The `TrustedContextBuilder` enforces a 7-step pre-generation pipeline:
1. **AUTHORIZE**: Evaluate user identity, organization scope, and workspace permissions.
2. **RETRIEVE**: Search Knowledge Fabric & Semantic Graph.
3. **CLASSIFY**: Apply DLP classification boundaries.
4. **RANK**: Weight relevance, source authority, and evidence coverage.
5. **CHECK FRESHNESS**: Evaluate TTL policy and flag stale objects.
6. **DETECT CONFLICTS**: Identify contradictory claims across retrieved items.
7. **ASSEMBLE EVIDENCE**: Format structured context items with source, authority, and classification tags.
