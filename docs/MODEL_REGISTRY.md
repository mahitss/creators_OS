# Model Registry & Provider Infrastructure

The Model Registry maintains verified metadata for supported model providers and candidate models in Vapor OS.

## Supported Providers
- **Google Vertex AI / Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash
- **OpenAI Enterprise**: GPT-4o, GPT-4o-mini
- **Anthropic Claude**: Claude 3.5 Sonnet

## Model Attributes
- `model_key`: Immutable unique identifier
- `provider_id`: Reference provider
- `capabilities`: Verified capability list (`text_generation`, `reasoning`, `tool_calling`, `structured_output`, `vision`, `long_context`, `code_generation`, `embedding`, `reranking`)
- `context_window`: Maximum token capacity
- `status`: `available`, `degraded`, `unavailable`, `disabled`, `deprecated`
