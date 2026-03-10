# AGENTS Asset Governance

## Status
- This document is the current non-executable governance source for AGENTS asset shape.
- The previous CLI implementation has been removed.
- New tooling must be rebuilt against this model instead of reusing the removed scripts.

## Split Model
- Internal human template must contain two explicit HTML-like blocks:

```html
<part_A>
...
</part_A>

<part_B>
...
</part_B>
```

- `Part A` is the only segment that may be written back to the external `AGENTS.md`.
- `Part B` stays inside the skill and must also be mirrored in the machine JSON.

## Scan
- `scan` only discovers which files are managed by this skill.
- It keeps the existing filename-driven discovery boundary.
- It does not write managed copies.

## Collect
- `collect` reads external managed `AGENTS.md` files.
- It extracts only the `<part_A> ... </part_A>` block.
- It updates only the internal human template's `Part A`.
- It must not overwrite the internal `Part B`.

## Push
- `push` reads the internal human template.
- It extracts only the `<part_A> ... </part_A>` block.
- It writes only that block back to the external `AGENTS.md`.
- `Part B` remains internal only.

## Maintenance Rule
- Any AGENTS governance change must be reviewed against both `Part A` and `Part B`.
- Do not update only one side unless the user explicitly scopes the change and the other side is proven unaffected.
- If payload shape or field structure changes, update human template, machine JSON, and future tool design together.

## Scope Note
- External root `AGENTS.md` and its corresponding internal root managed assets were excluded from this cleanup round.
