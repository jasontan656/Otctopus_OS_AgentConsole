---
doc_id: functional_humenworkzone_manager.tooling.cli_toolbox_development
doc_type: topic_atom
topic: Development entry for the Functional-HumenWorkZone-Manager CLI toolbox
anchors:
- target: Cli_Toolbox_USAGE.md
  relation: pairs_with
  direction: lateral
  reason: Usage and development docs are paired.
---

# Cli_Toolbox 开发文档（入口）

适用技能：`Functional-HumenWorkZone-Manager`

## 命名约束
- 本 skill 当前提供 `contract`、`directive`、`paths` 三个命令。

## 当前实现结构
- 入口脚本：`scripts/Cli_Toolbox.py`
- 运行合同根：`references/runtime_contracts/`
- 当前 runtime asset：
  - `SKILL_RUNTIME_CONTRACT`
  - `TASK_ROUTING_GUIDE`
  - `EXECUTION_BOUNDARY_CONTRACT`

## 文档分类规则
- `scripts/Cli_Toolbox.py` 只负责稳定输出 JSON payload，不在脚本里重复实现 markdown 规则树。
- 分支语义仍以下沉文档为主，但模型必须先经由 runtime contract 的 CLI JSON 做入口收敛。
- 新增 runtime-facing contract/workflow/instruction/guide 时，必须继续遵守 `*_human.md + same-name .json` 双文件形态。

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `references/runtime_contracts/*.json`
  - `references/runtime_contracts/*_human.md`
  - `SKILL.md`
  - `agents/openai.yaml`
- 若工具会影响 facade / routing / atomic doc tree，必须同步更新 `references/routing/` 与 `references/governance/`。

## 版本变更记录
- `2026-03-13`：补齐真实 `Cli_Toolbox.py`、runtime contracts 双文件资产与 CLI-first 门面入口。
