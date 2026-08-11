# Skill Dependency Graph

`SkillDependency` links skills to required tools, models, knowledge domains, and sub-skills.

## Validation
- Before skill activation, the runtime validates that all required tools, models, and knowledge objects exist and are active.
- Schema changes in dependent tools mark dependent skills as `needs_revalidation`.
