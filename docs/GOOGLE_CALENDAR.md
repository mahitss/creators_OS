# Vapor OS — Google Calendar Intelligence Architecture

## 1. Overview
Google Calendar Intelligence provides read-only calendar context for Vapor OS workspaces without requiring write permissions.

## 2. OAuth Scope Policy
Vapor requests strictly read-only Calendar permissions:
- Scope: `https://www.googleapis.com/auth/calendar.readonly`
- Zero event creation, editing, deletion, or meeting invitation permissions.

## 3. Synchronization Window & Incremental Sync
- **Active Window**: Previous 7 days to Next 30 days.
- **Incremental Sync**: Google Calendar sync tokens (`sync_token`) are persisted per calendar to fetch delta updates efficiently.

## 4. Privacy & AI Context Minimization
Before passing calendar commitments as context to AI operations (Executive Brief & Mission Planning), fields are strictly minimized:
- Included: `title`, `start_at`, `end_at`, `timezone`, `is_all_day`.
- Strictly Excluded: Attendee email addresses, private description notes, attachments, meeting passwords, or conference URLs.
