# Graph Schema & Relationship Types

## Supported Entity Types
`user`, `team`, `workspace`, `organization`, `project`, `mission`, `task`, `workflow`, `workflow_run`, `agent`, `agent_run`, `document`, `knowledge_source`, `artifact`, `integration`, `integration_action`, `event`, `incident`, `decision`, `recommendation`, `policy`, `security_finding`.

## Supported Relationship Types
- Structural: `belongs_to`, `member_of`, `owns`, `manages`, `contains`
- Execution: `depends_on`, `uses`, `created_by`, `assigned_to`, `triggered_by`, `triggered`, `caused_by`
- Semantic: `related_to`, `references`, `produces`, `consumes`, `supports`, `implements`, `blocked_by`, `reviewed_by`, `approved_by`, `derived_from`
