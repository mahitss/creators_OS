# Workflow Versioning & Immutability

## Draft vs Published Versions
- Editing an active workflow automatically creates a new `WorkflowVersion` draft.
- Active workflow runs reference an exact immutable `WorkflowVersion` and `compiledGraph`.
- Running workflows never execute unvalidated draft changes.
