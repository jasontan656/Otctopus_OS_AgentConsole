# Scan Rules

- Scan remains a discovery-only phase.
- Scan must not create or overwrite managed copies.
- Scan must read blacklists and keyword rules from external scan rule assets.
- `AGENTS.md` is currently the only governed filename that requires structure lint.
- If a new governed filename is added later, a matching structure template must exist before scan may pass.
- Missing structure templates are hard errors, not warnings.
