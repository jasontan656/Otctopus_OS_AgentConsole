Opt-out Markers (Automation Integration)

Goal
- Allow automated workflows to disable the meta mindchain deterministically, without relying on fuzzy skill matching.

How to disable
- Add one of the following tokens to the user prompt (anywhere):
  - `NO_META`
  - `AUTOMATION_MODE`
  - `WORKFLOW_AUTOMATION`

Expected behavior
- If any opt-out marker is present, do not apply the meta-chain.
- Respond normally without referencing this skill or its framework.

Recommended usage patterns
- Interactive sessions: omit opt-out markers (meta-chain enabled by default).
- Automated workflows: prepend `AUTOMATION_MODE` to the prompt template.

