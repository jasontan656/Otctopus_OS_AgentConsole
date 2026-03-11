---
doc_id: "skill_creation_template.tooling.architecture_overview"
doc_type: "tooling_architecture"
topic: "Architecture overview for the skill template toolbox and generator"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc is routed from the development entry."
  - target: "../../governance/SKILL_ARCHITECTURE_PLAYBOOK.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "The toolbox architecture follows the same architecture playbook."
  - target: "modules/create_skill_from_template.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Module-level implementation details continue in the module doc."
---

# Cli_Toolbox 开发文档架构总览

## 目标
- 让模板技能的脚本、contracts、assets、tooling 文档与测试围绕同一套门面结构治理。
- 保证 `create_skill_from_template.py` 生成的不是“占位文档集合”，而是可直接继续收敛的 skill control plane。
- 保证 `basic` 与 `staged_cli_first` 共享统一门面哲学，但输出不同深度的合同面。

## 分层结构
0. 技能门面层：`SKILL.md`
1. 运行合同层：`references/runtime/`
2. 路由与治理层：
   - `references/routing/`
   - `references/governance/`
3. 工具入口层：
   - `scripts/Cli_Toolbox.py`
   - `scripts/create_skill_from_template.py`
4. 模板资产层：
   - `assets/skill_template/`
5. 校验层：
   - `tests/`

## 当前关键设计
- 默认门面采用极简 facade，并把深规则下沉到 routing / governance docs。
- `skill-doc-structure` 已进入模板包的显式治理合同。
- `staged_cli_first` 默认生成 runtime contract 和 stage template kit。
- stage template kit 包含：
  - `CHECKLIST.json`
  - `DOC_CONTRACT.json`
  - `COMMAND_CONTRACT.json`
  - `GRAPH_CONTRACT.json`
- 默认资源目录包含 `tests/`，为模板回归预留位置。

## 维护原则
- 先改 runtime contract 与 routing/governance 文档树，再改模板资产，再改生成器，再补工具文档与测试。
- 若改动的是 staged profile，必须把合同面和模板 kit 一起改完，不能只改 `SKILL_TEMPLATE_STAGED.md`。
- 若脚本与文档描述不一致，以脚本行为为准并立即回写文档；不要保留“双真相”。
