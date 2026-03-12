# Root File Mapped Copy Structure

- This file defines the governed internal mapping shape for non-`AGENTS.md` root files.

## Scope
- Applies to every non-`AGENTS.md` channel registered in `rules/scan_rules.json`.
- Does not redefine `AGENTS.md` A/B semantics.

## Internal Mapping Naming Rule
- Internal mapped copies must not reuse the external filename directly.
- Internal mapped copies must carry explicit mapping semantics in the filename.
- Recommended pattern:
  - `<CHANNEL_ID>__governed_external.<ext>`
  - or an equivalent channel-specific filename declared in the channel registry

## Content Rule
- Internal mapped copy content must equal the external root file content byte-for-byte at the text level.
- No wrapper header may be injected for these non-`AGENTS.md` mapped copies.
- The “this is an internal governed mapping version” meaning is expressed by:
  - the channel registry
  - the managed asset path
  - the managed filename

## Lint Rule
- `lint` must fail when the mapped copy is missing.
- `lint` must fail when the mapped copy content drifts from the external file content.

## Push / Collect Rule
- `collect` reads the external file and overwrites the internal mapped copy.
- `push` reads the internal mapped copy and overwrites the external file.
