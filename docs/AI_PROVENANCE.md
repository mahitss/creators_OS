# AI Output Provenance & Quality Feedback

## AI Output Tracking
`AIOutputProvenance` records `output_id`, `model`, `model_version`, `prompt_version`, `context_references`, `generated_at`, and `evaluation_status`.

## Quality Feedback
Operators can submit feedback (`correct`, `incorrect`, `outdated`, `missing_source`, `conflicting`). Negative feedback automatically downgrades output evaluation status to `unsupported` and feeds evaluation signals.
