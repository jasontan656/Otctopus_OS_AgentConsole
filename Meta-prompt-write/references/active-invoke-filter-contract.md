# Active Invoke Filter Contract (Meta-prompt-write)

## Contract ID
`active_invoke_filter_contract_v3`

## Purpose
固定 `Meta-prompt-write` 的最终输出形态。
它只做一件事：把已经补足的 `raw_prompt_output` 压成稳定的结构化执行合同模板。

## Script
- Path: `/home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py`
- Supported modes:
  - `active_invoke`
  - `skill_directive`

## Active Invoke Output Shape
```text
GOAL:
...

REPO_CONTEXT_AND_IMPACT:
- ...

INPUTS:
- ...

OUTPUTS:
- ...

BOUNDARIES:
- ...

VALIDATION:
- ...
```

## Rules
- 最终输出必须固定为 6 段。
- 不允许自由增删段名。
- 不允许输出方法论报告、风险矩阵、复盘说明、mode router 元信息。
- `skill_directive` 仅用于 AGENTS / runtime 的“读 skill”提示。

## Exit Codes
- `0`: success
- `10`: template_missing
- `11`: invalid_output
- `12`: empty_after_filter
- `13`: skill_source_missing
