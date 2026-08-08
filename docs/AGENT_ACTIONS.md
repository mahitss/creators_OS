# Vapor OS — Real Agent Actions & Tool Risk Policy

## 1. Overview
Sprint 21 introduces real write and external action tools to Vapor OS Agent Runtime governed by strict human-in-the-loop approval gates.

## 2. Centralized Risk Policy Matrix
- `READ`: Automatic tool execution (`search_missions`, `get_calendar_events`, `search_drive_files`).
- `WRITE`: Internal state mutations (`create_mission`, `create_content`, `update_content`, `create_memory_candidate`) require explicit user approval.
- `EXTERNAL_SIDE_EFFECT`: External side-effects (`create_calendar_event`) require explicit user approval, input hash validation, conflict checks, and provider verification.
- `DESTRUCTIVE`: Blocked completely (`send_gmail`, `delete_file`, `modify_drive`).

## 3. Real Write & Action Tools
1. `create_mission`: Creates workspace Mission.
2. `create_content`: Creates Studio Content Canvas draft (`status="draft"`).
3. `update_content`: Updates draft title/body.
4. `create_memory_candidate`: Proposes Memory candidate (`status="pending"`).
5. `create_calendar_event`: Proposes Google Calendar event, checks conflicts, and verifies event ID on approval.
