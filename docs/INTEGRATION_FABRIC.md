# Enterprise Integration Fabric Architecture

## Controlled Integration Platform
Integrations are untrusted boundaries. All connections are managed through `Integration` and `IntegrationConnection` models with strict capability scoping. Raw credentials and tokens are encrypted and never exposed to agents or AI models.
