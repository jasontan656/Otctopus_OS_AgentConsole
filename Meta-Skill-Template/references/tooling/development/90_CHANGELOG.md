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
- 2026-03-09
  - 增加模板契约：若技能存在运行态规则、约束、指引，必须提供 CLI 输出入口与 machine-readable 合同；markdown 只做审计版。
  - 更新 `SKILL_TEMPLATE.md`、模板合同与架构手册，使模板同步支持 CLI-first 规则分发。
- 2026-03-09
  - 为 Meta-Skill-Template 自身补充 `scripts/Cli_Toolbox.py` 统一入口。
  - 将 `SKILL.md` 收缩为纯入口页，详细治理规则下沉到 runtime contract 与 references。
