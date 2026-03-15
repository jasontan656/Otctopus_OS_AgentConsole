---
doc_id: skillsmanager_tooling_checkup.path.cli_surface.contract
doc_type: topic_atom
topic: Contract for CLI surface checking
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: CLI surface contract is followed by the applicable tools.
---

# CLI Surface 检查合同

## 当前动作要完成什么
- 检查目标技能的本地 CLI 是否暴露了清晰稳定的受管入口。
- 检查 path 技能的 `read-contract-context` 是否真的能编译完整链路上下文。

## 当前动作必须满足什么
- 目标技能若存在受管 `scripts/` surface，应暴露一个明确的 `Cli_Toolbox` 入口。
- 带 `scripts/ + path/` 且不是 `guide_only` 的目标技能，需要提供可工作的 `read-contract-context`；`read-path-context` 可作为等价别名保留。
- `read-contract-context` 必须返回稳定的 JSON，至少包含：
  - `resolved_chain`
  - `segments`
  - `compiled_markdown`
- 不能要求目标技能复用本技能自己的 `contract / directive` 命名。

## 下一跳列表
- [tools]：`15_TOOLS.md`
