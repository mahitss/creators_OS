# Vapor OS — Google Drive Intelligence Architecture

## 1. Overview
Google Drive Intelligence enables read-only document metadata discovery, on-demand document text extraction, Mission document attachment (`MissionDocumentReference`), and grounded source citations.

## 2. OAuth Scope Policy
Vapor requests strictly read-only Drive permission:
- Scope: `https://www.googleapis.com/auth/drive.readonly`
- ZERO write, edit, rename, delete, share, or permission management capabilities.

## 3. Metadata Storage Policy & Bounded Extraction
- Metadata Storage: Only file metadata (`name`, `mime_type`, `description`, `web_url`, `size_bytes`, `modified_time`) is persisted by default.
- On-Demand Content Extraction: Full text is retrieved lazily only when explicitly requested. Extraction is capped at 50,000 characters to ensure safe AI context limits.

## 4. Grounded Source Citations
AI operations consuming attached Drive documents preserve source references:
- Included: `drive_file_id`, `file_name`, `web_url`, `mime_type`.
