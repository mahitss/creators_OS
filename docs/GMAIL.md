# Vapor OS — Gmail Intelligence Architecture

## 1. Overview
Gmail Intelligence provides read-only email triage, structured AI classification (`needs_response`, `important`, `informational`), grounded summarization, and single-click mission creation.

## 2. OAuth Scope Policy
Vapor requests strictly read-only Gmail scope:
- Scope: `https://www.googleapis.com/auth/gmail.readonly`
- ZERO permissions for email sending, replying, forwarding, deleting, or archiving.

## 3. Privacy-First Storage Policy
- Default Storage: Subject, sender name, sender email, snippet, received timestamp, thread ID, and label IDs.
- Full Body Storage: Fetched lazily on demand when the user opens a message. Full mailboxes are never copied.

## 4. AI Triage & Context Boundaries
- Structured Classification: Messages are categorized into `needs_response`, `important`, `informational`, or `low_priority`.
- AI Context Minimization: AI operations receive only minimal subject and snippet context. Raw mailbox dumps are strictly forbidden.

## 5. Mission Conversion
Users can convert an important email into a workspace Mission via `POST /api/v1/gmail/messages/{id}/create-mission` with explicit user confirmation.
