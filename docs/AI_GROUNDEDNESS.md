# AI Groundedness & Citation Validation

## Grounding Evaluation
AI responses undergo post-generation validation for citation accuracy and factual grounding:
- `grounded`: All citations match real, authorized evidence sources.
- `partially_grounded`: Some citations match; minor unsupported claims exist.
- `unsupported`: Claims produced without evidence references.
- `citation_error`: Response cites non-existent or unauthorized sources.
- `insufficient_evidence`: System explicitly states lack of verified information.
