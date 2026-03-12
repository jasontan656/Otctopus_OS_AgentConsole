# anchor_docs_machine

Machine-only constitution corpus for `Cli_Toolbox.constitution_keyword_query`.

## Files
- `anchor_docs_machine_v1.jsonl`: one JSON object per anchor rule.

## Schema (compact)
- `v`: machine schema version.
- `id`: anchor id.
- `cat`: `common_core|common_conditional|constraints`.
- `domain`: graph domain.
- `priority`: `always_on|query_hit`.
- `cohit`: required co-hit domains.
- `title_en`: compact english title.
- `keywords_en`: english match terms.
- `keywords_zh`: chinese match terms.
- `must`: required machine actions.
- `forbid`: forbidden machine actions.
- `gate`: gate conditions.
- `evidence`: required evidence fields.
- `src`: human markdown source path.

## Build
```bash
cd <repo-root> && ./.venv_backend_skills/bin/python Skills/Constitution-knowledge-base/scripts/build_machine_anchor_docs.py
```
