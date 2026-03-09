---
name: "Meta-Skill-Template"
description: "使用标准化模板创建或改造 Codex 技能描述文档；默认采用抽象层 + 业务需求层分域写法。"
---

# Meta-Skill-Template

## 1. 目标
- 提供统一的 Codex 技能模板入口，负责创建或改造技能骨架。
- 支持两类模板 profile：
  - `basic`
  - `staged_cli_first`
- 模板默认要求未来技能采用：
  - 抽象层
  - 业务需求层
- 保持 `SKILL.md` 轻量，仅承载入口、边界和导航。

## 2. 可用工具
- 抽象层：
  - 统一工具入口：`scripts/Cli_Toolbox.py`
  - 统一入口命令：
    - `create-skill-from-template`
      - 作用：按模板创建或改造技能骨架。
    - `runtime-contract`
      - 作用：输出本技能自身运行合同。
    - `contract-reference`
      - 作用：输出模板契约参考。
    - `architecture-playbook`
      - 作用：输出模板架构手册。
- `basic`：
  - `skill-template`
    - 作用：输出基础技能门面模板。
  - `openai-template`
    - 作用：输出 `agents/openai.yaml` 模板。
- `staged_cli_first`：
  - `staged-skill-template`
    - 作用：输出复杂技能门面模板。
  - `staged-skill-reference`
    - 作用：输出复杂技能 profile 提炼参考。
  - `runtime-contract-template`
    - 作用：输出复杂技能 runtime contract 模板。
- 抽象功能可共享；业务域或阶段域命令必须独立，不得串用。
- 详细工具说明下沉到 `references/tooling/`。

## 3. 工作流约束
- 抽象层：
  - 进入技能后，先读取 `runtime-contract` 明确本技能运行边界。
  - 创建或改造技能时，优先走 `create-skill-from-template`。
  - 未来生成的技能默认采用“抽象层 + 业务需求层”的分域写法。
- `basic`：
  - 使用 `create-skill-from-template --profile basic`。
  - 生成后的 `SKILL.md` 必须在 `3/4/5/6` 段显式拆成：
    - 抽象层
    - 业务需求层
- `staged_cli_first`：
  - 使用 `create-skill-from-template --profile staged_cli_first`。
  - 若需查看复杂技能规则，读取：
    - `staged-skill-reference`
    - `architecture-playbook`
  - 生成后的 `SKILL.md` 必须在 `3/4/5/6` 段显式拆成：
    - 抽象层
    - 各业务阶段域

## 4. 规则约束
- 抽象层：
  - 本页禁止继续承载堆积式治理细节。
  - 详细模板契约、架构规则、tooling 规则统一下沉到 `references/`。
  - 所有规则必须先分域，再写各域抽象通用规则与域内细则。
  - 禁止任何可能的混写。
- `basic`：
  - 业务需求层即便只有一个域，也必须显式独立成域，不得与抽象层混写。
  - 业务域命令不得复用为其他域命令名。
- `staged_cli_first`：
  - 各阶段必须各写各的形态，不得混写。
  - 顶层规则属于 always-load 规则；阶段域规则不得覆盖顶层规则。
  - 统一 CLI 入口可共享，但各阶段命令必须独立。
- 若治理规则变化，必须同步更新本页入口、runtime contract、tooling 文档与模板资产。

## 5. 方法论约束
- 抽象层：
  - 先确定技能运行态目标，再套用模板骨架。
  - 优先通过统一 CLI 入口访问模板资源，避免分散入口漂移。
  - 运行态规则优先 CLI-first；结构化 markdown 只做人类审计与分域导航。
- `basic`：
  - 先抽象，再落业务域，不把二者混成一个段落。
  - 若只有单业务域，也按“抽象层 + 单域”显式写法组织。
- `staged_cli_first`：
  - 先抽象，再按阶段域拆分。
  - 抽象功能可共享；特定阶段命令禁止共享。
  - 任意部分都采用“抽象层 + 独立域”的写法。

## 6. 内联导航索引
- 抽象层：
  - [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
  - [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
  - [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
  - [模板契约] -> [references/skill_template_contract_v1.md]
  - [架构手册] -> [references/skill_architecture_playbook.md]
  - [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
  - [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- `basic`：
  - [基础模板资产] -> [assets/skill_template/SKILL_TEMPLATE.md]
  - [openai 模板] -> [assets/skill_template/openai_template.yaml]
- `staged_cli_first`：
  - [复杂技能 profile 提炼] -> [references/staged_cli_first_profile_reference.md]
  - [复杂技能模板资产] -> [assets/skill_template/SKILL_TEMPLATE_STAGED.md]
  - [runtime 模板资产] -> [assets/skill_template/runtime/]
  - [stages 模板资产] -> [assets/skill_template/stages/]

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
│       ├── SKILL_TEMPLATE_STAGED.md
│       ├── openai_template.yaml
│       ├── Cli_Toolbox_USAGE_TEMPLATE.md
│       ├── Cli_Toolbox_DEVELOPMENT_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_ARCHITECTURE_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_MODULE_CATALOG_TEMPLATE.yaml
│       ├── Cli_Toolbox_DEV_CATEGORY_INDEX_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_MODULE_TEMPLATE.md
│       ├── Cli_Toolbox_DEV_CHANGELOG_TEMPLATE.md
│       ├── runtime/
│       └── stages/
└── references/
    ├── runtime/
    │   ├── SKILL_RUNTIME_CONTRACT.json
    │   └── SKILL_RUNTIME_CONTRACT.md
    ├── skill_template_contract_v1.md
    ├── staged_cli_first_profile_reference.md
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
