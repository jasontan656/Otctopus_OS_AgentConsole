---
doc_id: "skill_creation_template.tooling.changelog"
doc_type: "changelog"
topic: "Change log for the skill template toolbox and governance pack"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The changelog belongs to the development references set."
  - target: "../../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "tracks_changes_to"
    direction: "cross"
    reason: "Runtime contract changes must be traceable in the changelog."
---

# Cli_Toolbox 开发文档变更记录

- 2026-02-25
  - 将开发文档从单文件升级为“入口 + 分类 + 模块”结构。
- 2026-02-26
  - 澄清生成技能的 `1.目标` 只能写运行态目标，不能写“创建技能本身”。
- 2026-03-09
  - 引入 `staged_cli_first` profile，并为复杂技能补齐 runtime contract 与 stage template kit。
- 2026-03-10
  - 将模板门面统一升级为 7 段 façade：
    - `定位`
    - `必读顺序`
    - `分类入口`
    - `适用域`
    - `执行入口`
    - `读取原则`
    - `结构索引`
  - staged 模板 kit 新增 `CHECKLIST.json`，并把 resident docs、阶段合同四件套和 discard policy 升为模板硬约束。
  - `create_skill_from_template.py` 默认资源新增 `tests/`。
  - 引入生成回归测试，确保 profile 输出面不漂移。
- 2026-03-11
  - 将模板技能自身重构为 `facade + routing + topic docs + index` 的文档树。
  - 将 `skill-doc-structure` 写入 runtime contract、authoring contract、playbook 与模板资产，升为显式执行合同。
  - basic / staged 模板生成结果新增 task routing、doc-structure policy 与 execution rules。
  - tooling 文档、生成器与回归测试同步切换到新结构。
