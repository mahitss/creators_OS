# Secure AI Retrieval & Double Authorization Filter Gate

## Core Principle: Vector Similarity Is Never Authorization
Vector distance scores indicate semantic relevance, NOT authorization. Every candidate returned by vector similarity search proceeds through an explicit Authorization Filter Gate (checking organization, workspace, user role, resource permission, classification ceiling, and PolicyEngine policies) followed by a DLP Filter Gate before being rendered or transmitted to AI models.
