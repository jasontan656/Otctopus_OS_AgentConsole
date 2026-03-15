---
doc_id: skillsmanager_doc_structure.path.primary_flow.tools
doc_type: topic_atom
topic: Tool or lint surface for the primary doc-structure governance flow
anchors:
- target: 10_CONTRACT.md
  relation: implements
  direction: upstream
  reason: Tooling follows the contract.
- target: 20_EXECUTION.md
  relation: routes_to
  direction: downstream
  reason: Execution follows after the tool surface is clear.
---

# 主治理链路 Tool/Lint 能力面

## 当前动作要用什么命令
- `python3 ./scripts/Cli_Toolbox.py inspect-target --target <skill_root> --json`
- `python3 ./scripts/Cli_Toolbox.py lint-root-shape --target <skill_root> --json`
- `python3 ./scripts/Cli_Toolbox.py lint-reading-chain --target <skill_root> --json`
- `python3 ./scripts/Cli_Toolbox.py build-anchor-graph --target <skill_root> --json`
- `python3 ./scripts/Cli_Toolbox.py lint-docstructure --target <skill_root> --json`

## 当前动作如何理解这些命令
- `inspect-target`：只判定目标技能的组织形态，不下结论。
- `lint-root-shape`：只检查根目录是否还挂着不该存在的主组织轴。
- `lint-reading-chain`：检查 `SKILL.md -> path -> entry -> next hop` 是否逐级向下。
- `build-anchor-graph`：抽取当前技能或目标技能的 anchors 图。
- `lint-docstructure`：汇总根形态、链路和 anchors 的错误。
- 语义检查：由模型沿当前技能自己的 path 规则阅读目标技能，再判断各层正文是否承担了正确职责。

## 下一跳列表
- [执行]：`20_EXECUTION.md`
