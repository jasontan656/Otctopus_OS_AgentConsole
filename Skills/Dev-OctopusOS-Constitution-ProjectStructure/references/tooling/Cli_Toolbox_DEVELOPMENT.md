---
doc_id: "dev_octopusos_constitution_projectstructure.tooling.toolbox_development"
doc_type: "topic_atom"
topic: "Tooling development status for the OctopusOS project-structure constitution skill"
anchors:
  - target: "Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Development and usage docs must stay aligned."
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Tooling development should route into the architecture overview."
---

# Cli_Toolbox Development

## 当前状态
- 本技能当前没有专属 CLI，也没有工具开发模块。

## 后续开发约束
- 若未来新增工具，不得绕开当前 skill 的项目级结构合同自行发明 lint 口径。
- 工具模块、usage docs、development docs 与 registry/skill 文档必须同回合同步。
