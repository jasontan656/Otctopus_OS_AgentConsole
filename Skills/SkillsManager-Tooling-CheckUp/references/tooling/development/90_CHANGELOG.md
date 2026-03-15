---
doc_id: skills_tooling_checkup.tooling.changelog
doc_type: topic_atom
topic: Changelog for the skills tooling checkup control plane
---

# Tooling Changelog

- `2026-03-12`
  - 基于 `basic` profile 创建 `SkillsManager-Tooling-CheckUp`。
  - 明确本技能无本地 `Cli_Toolbox.py`，只治理已安装 skills 的 tooling code 是否绕开既定依赖栈自造轮子。
  - 新增依赖基线与修正协议两份原子治理文档。
- `2026-03-12`
  - 新增 `OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md`，把 runtime 日志根目录、result 产物根目录、定向产物显式落点、文档声明要求与历史迁移责任纳入语义治理。
  - 更新 routing / execution / gates / patterns / tooling docs，使该治理轴线成为正式入口而非临时口头约定。
- `2026-03-12`
  - 新增本地 `scripts/Cli_Toolbox.py`，提供 `contract` 与 `directive` 双入口。
  - 新增 `references/runtime_contracts/`，把 runtime-facing contract/workflow/instruction/guide 治理为 `*_human.md + same-name .json`。
  - 将技能门面与 agent prompt 切换为 CLI-first，明确模型必须先吃 JSON payload，不再通过 markdown 路径链寻找规则。
- `2026-03-12`
  - 新增 `govern-target` 入口，专门对目标 skill 输出 tooling surface 审计结果。
  - 明确 `govern-target` 只治理 CLI / runtime-facing assets / 输出治理，不承担目标技能形态治理。
