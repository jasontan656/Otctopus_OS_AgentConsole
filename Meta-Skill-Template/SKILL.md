---
name: "Meta-Skill-Template"
description: "使用标准化模板创建或改造 Codex 技能描述文档；本页只保留入口、边界和导航，详细治理规则下沉到 runtime contract 与 references。"
---

# Meta-Skill-Template

## 1. 目标
- 提供统一的 Codex 技能模板入口，负责创建或改造技能骨架。
- 保持 `SKILL.md` 轻量，仅承载路由、边界与导航。

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- 主要命令：
  - `create-skill-from-template`
  - `skill-template`
  - `openai-template`
  - `contract-reference`
  - `architecture-playbook`
  - `runtime-contract`
- 详细工具说明下沉到 `references/tooling/`。

## 3. 工作流约束
- 进入技能后，先读取 `runtime-contract` 明确本技能运行边界。
- 创建或改造技能时，优先走 `create-skill-from-template`。
- 若需查看模板契约或架构规则，读取 `contract-reference` 与 `architecture-playbook` 对应资源。

## 4. 规则约束
- 本页禁止继续承载堆积式治理细节。
- 详细模板契约、架构规则、tooling 规则统一下沉到 `references/`。
- 若治理规则变化，必须同步更新本页入口、runtime contract、tooling 文档与模板资产。

## 5. 方法论约束
- 先确定技能运行态目标，再套用模板骨架。
- 优先通过统一 CLI 入口访问模板资源，避免分散入口漂移。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [模板契约] -> [references/skill_template_contract_v1.md]
- [架构手册] -> [references/skill_architecture_playbook.md]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [模板资产] -> [assets/skill_template/SKILL_TEMPLATE.md]

## 7. 架构契约
```text
Meta-Skill-Template/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   └── create_skill_from_template.py
├── assets/
│   └── skill_template/
│       ├── SKILL_TEMPLATE.md
│       ├── openai_template.yaml
│       ├── Cli_Toolbox_USAGE_TEMPLATE.md
│       ├── Cli_Toolbox_DEVELOPMENT_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_ARCHITECTURE_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_MODULE_CATALOG_TEMPLATE.yaml
│       ├── Cli_Toolbox_DEV_CATEGORY_INDEX_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_MODULE_TEMPLATE.md
│       └── Cli_Toolbox_DEV_CHANGELOG_TEMPLATE.md
└── references/
    ├── runtime/
    │   ├── SKILL_RUNTIME_CONTRACT.json
    │   └── SKILL_RUNTIME_CONTRACT.md
    ├── skill_template_contract_v1.md
    ├── skill_architecture_playbook.md
    └── tooling/
        ├── Cli_Toolbox_USAGE.md
        ├── Cli_Toolbox_DEVELOPMENT.md
        └── development/
            ├── 00_ARCHITECTURE_OVERVIEW.md
            ├── 10_MODULE_CATALOG.yaml
            ├── 20_CATEGORY_INDEX.md
            ├── 90_CHANGELOG.md
            └── modules/
                ├── MODULE_TEMPLATE.md
                └── create_skill_from_template.md
```
