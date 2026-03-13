---
doc_id: dev_octopusos_constitution_projectstructure.tooling.toolbox_development
doc_type: topic_atom
topic: Tooling development status for the OctopusOS project-structure constitution skill
anchors:
- target: Cli_Toolbox_USAGE.md
  relation: pairs_with
  direction: lateral
  reason: Development and usage docs must stay aligned.
- target: development/00_ARCHITECTURE_OVERVIEW.md
  relation: routes_to
  direction: downstream
  reason: Tooling development should route into the architecture overview.
---

# Cli_Toolbox Development

## 当前状态
- 本技能当前已有静态 `Cli_Toolbox.py`，职责仅限于输出 runtime contract。
- 当前工具不是 lint/registry 检查器，不直接裁决仓内结构；它只把治理入口、读取顺序和命名宪法稳定暴露给运行时。

## 后续开发约束
- 若未来新增工具，不得绕开当前 skill 的项目级结构合同自行发明 lint 口径。
- 工具模块、usage docs、development docs 与 registry/skill 文档必须同回合同步。
