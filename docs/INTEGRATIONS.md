# Vapor OS — Integrations Foundation Architecture

## 1. Overview
The Integrations Foundation provides a secure, workspace-isolated connection lifecycle for external identity and service providers.

## 2. Supported Provider Abstraction
Controlled enum:
- `google`: Reference implementation (Identity & OAuth 2.0)
- Planned: `github`, `youtube`, `slack`, `notion`, `calendar`, `gmail`

## 3. Database Schema
- `IntegrationConnection`: Stores workspace connection state (`connected`, `expired`, `revoked`, `error`, `disconnected`), scopes, external account identity, and Fernet encrypted access/refresh tokens.
- `IntegrationSyncJob`: Light job record tracking background synchronization runs (`queued`, `running`, `completed`, `failed`, `cancelled`).

## 4. Minimum Scope Policy
Integrations request only the minimum required scopes:
- Google: `openid`, `email`, `profile`. Zero broad or destructive permissions (`gmail.write`, `drive.delete`).
