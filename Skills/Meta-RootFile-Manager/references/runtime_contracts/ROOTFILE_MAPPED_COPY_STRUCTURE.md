---
doc_id: meta_rootfile_manager.references_runtime_contracts_rootfile_mapped_copy_structure
doc_type: topic_atom
topic: Root File Mapped Copy Structure
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

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
- Internal mapped copy remains the manager-owned source of truth for `push`.
- Every governed target must carry `owner` inside the existing managed content surface itself.
- `owner` is derived from the governed directory meaning plus the current channel semantics; it is descriptive text, not a fixed enum.
- If the managed content is a json object, `owner` must be injected into that json object itself.
- If the managed content is not json, `owner` must be injected through frontmatter in the same managed file.
- The “this is an internal governed mapping version” meaning is expressed by:
  - the channel registry
  - the managed asset path
  - the managed filename
  - the embedded owner field in the managed file itself

## Lint Rule
- `lint` must fail when the mapped copy is missing.
- `lint` must fail when the embedded `owner` is missing.
- `lint` must fail when the mapped copy content drifts from the external file content after stripping manager-owned owner metadata from the managed file.
- `lint` must fail when the stored `owner` no longer matches the path-derived owner description.

## Push / Collect Rule
- `collect` reads the external file, derives `owner`, and refreshes the internal mapped copy by embedding `owner` into the same managed file.
- `push` reads the internal mapped copy and overwrites the external file; manager-owned owner metadata may stay internal-only for non-`AGENTS.md` markdown channels.
