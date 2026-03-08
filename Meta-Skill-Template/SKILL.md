---
name: "Meta-Skill-Template"
description: 使用标准化模板创建或改造 Codex 技能描述文档；强制采用 1-7 章节完整结构，并要求运行态指引优先由 CLI 输出。
---

# Meta-Skill-Template

## 1. 目标
- 提供统一的技能描述文档结构，避免“每个技能写法都不一样”。
- 以最小必要信息驱动模型执行，避免说明文档横向膨胀。
- 支持对新建技能和存量技能做同构化改写。
- 当技能存在运行态规则、约束、指引时，模板必须要求通过 CLI 输出 machine-readable 合同，而不是让模型直接读 markdown。

## 2. 可用工具
- 本节条目必须保留：若技能不包含任何工具，填写“本技能无工具（N/A）”。
- 统一命名约束：技能内工具统一使用前缀 `Cli_Toolbox`。
- 工具清单（本技能）：
  - `Cli_Toolbox.create_skill_from_template` - "使用 `--skill-name/--target-root/--resources/--description/--overwrite` 参数创建或更新技能骨架；预期输出为结构化 JSON（`skill_dir`、`resources_created`、`write_results`），用于格式化目标结构正文与资源目录。"
  - `Cli_Toolbox.skill_template` - "提供 `SKILL.md` 的 1-7 章节正文模板，用于快速生成目标结构内 body 正文，避免缺章或顺序错乱。"
  - `Cli_Toolbox.openai_template` - "提供 `agents/openai.yaml` 的接口字段基线（`display_name`、`short_description`、`default_prompt`），用于标准化元数据输出结构。"
  - `Cli_Toolbox.contract_reference` - "用于查询与对照技能契约规则，重点检查必选章节、可选章节与验收项，预期输出为可执行的规则清单。"
  - `Cli_Toolbox.architecture_playbook` - "用于对描述文档与工具文档做结构审查与 lint 导向核对（如职责边界、禁用写法、可验证字段约束）。"
- 文档同步约束（强制）：
  - 每个技能内工具都必须存在对应“使用文档”和“开发文档”。
  - 推荐路径：`references/tooling/Cli_Toolbox_USAGE.md` 与 `references/tooling/Cli_Toolbox_DEVELOPMENT.md`。
  - 工具变更时必须同步更新两类文档，禁止只改代码不改文档。
  - `Cli_Toolbox_USAGE.md` 必须采用“人类叙事版输入 -> 电脑动作发生了什么 -> 人类叙事版输出”的固定叙事格式。
  - `Cli_Toolbox_USAGE.md` 目标读者包含老板/PM/AI：内容必须人类可读且机器可执行，不允许只写参数清单。
  - `Cli_Toolbox_USAGE.md` 必须提供“示例命令（强制）”章节：命令必须以 `cd <skill_root> &&` 开头、保持一行可复制、包含管道，并附一条最小用途描述。
  - 若技能包含运行态规则、约束、指引，必须额外提供 CLI 输出入口与 machine-readable 合同；markdown 只做审计镜像。
- 开发文档结构化约束（用于复杂 Toolbox）：
  - 开发文档不得长期承载为单一胖文件；必须拆分为“入口 + 分类 + 模块”结构。
  - 入口文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`（提供内联索引与阅读顺序）。
  - 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`。
  - 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`。
  - 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`。
  - 模块模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`。

## 3. 工作流约束
- 当任务需要流程化执行时，建议包含本节。
- 若包含，需明确输入、步骤、输出和完成判定。
- 若技能存在运行态规则，应在本节显式给出 machine-readable 合同入口、CLI 入口与 markdown 审计入口。
- 若暂不适用，可保留标题并填写 `N/A（当前无工作流约束）`。

## 4. 规则约束
- 当任务存在强规则（命名、边界、门禁、禁止项）时，建议包含本节。
- 规则描述应可验证，避免仅口号式表述。
- 生成技能的 `1.目标` 必须描述“技能运行态目标”，不得写入“创建技能本身/改模板本身”的建模流程目标。
- 若技能存在运行态规则、约束、指引，必须满足：
  - 模型禁止直接阅读 markdown 获取运行指引。
  - 运行指引必须由 CLI 输出。
  - 规则必须同时存在 markdown 与 json/yaml 两份。
  - 规则更新时必须同步更新两份，且建议以 machine-readable 合同为源刷新 markdown。
- 若暂不适用，可保留标题并填写 `N/A（当前无规则约束）`。

## 5. 方法论约束
- 当需要固定思维方式或推理顺序时，建议包含本节。
- 优先写“何时使用/何时不使用”，避免泛化空话。
- 当技能存在运行态规则时，优先采用“先 contract，再 directive，再动作”的 CLI-first 模式。
- 若暂不适用，可保留标题并填写 `N/A（当前无方法论约束）`。

## 6. 内联导航索引
- 该索引必须直接出现在 `SKILL.md`，并可一跳跳转到关键资源。
- 推荐最小索引项：
  - `Cli_Toolbox 工具入口` -> `scripts/create_skill_from_template.py`
  - `模板资产` -> `assets/skill_template/SKILL_TEMPLATE.md`
  - `契约文档` -> `references/skill_template_contract_v1.md`
  - `架构手册` -> `references/skill_architecture_playbook.md`
  - `Cli_Toolbox 使用文档` -> `references/tooling/Cli_Toolbox_USAGE.md`
  - `Cli_Toolbox 开发文档` -> `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - `Cli_Toolbox 开发架构总览` -> `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
  - `Cli_Toolbox 开发分类索引` -> `references/tooling/development/20_CATEGORY_INDEX.md`
  - `Cli_Toolbox 模块目录` -> `references/tooling/development/10_MODULE_CATALOG.yaml`

## 7. 架构契约
当前技能真实目录结构（应保持与实现同步）：

```text
Meta-Skill-Template/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
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

落地规则：
- `1-7` 章节条目必须完整存在，不得缺失标题。
- `2/3/4/5` 为可选填充章节：可填写完整约束，也可明确标注 `N/A`。
- `7` 作为结构定义章节应保留，用于保障目录与文档同构。
