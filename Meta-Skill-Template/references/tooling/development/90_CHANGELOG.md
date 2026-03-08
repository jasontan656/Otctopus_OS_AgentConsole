# Cli_Toolbox 开发文档变更记录

- 2026-02-25
  - 将开发文档从单文件升级为“入口 + 分类 + 模块”结构。
  - 新增：
    - `00_ARCHITECTURE_OVERVIEW.md`
    - `10_MODULE_CATALOG.yaml`
    - `20_CATEGORY_INDEX.md`
    - `modules/MODULE_TEMPLATE.md`
    - `modules/create_skill_from_template.md`
- 2026-02-26
  - 澄清模板语义：被创建技能的 `1.目标` 仅允许写运行态目标，不得写“创建技能本身”。
  - 调整 `create_skill_from_template.py` 默认 `description/default_prompt`，避免把建模流程目标注入生成技能。
