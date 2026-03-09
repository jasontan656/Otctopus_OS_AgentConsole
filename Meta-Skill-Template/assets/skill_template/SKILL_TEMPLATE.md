---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 目标
- [描述此技能在运行态要解决的业务问题，不要写“创建/生成本技能”这类建模流程目标。]
- [未来生成技能默认采用“抽象层 + 业务需求层”写法。]

## 2. 可用工具
- 抽象层：
  - [列出统一工具入口、共享工具能力、抽象辅助命令。]
  - 命名规则：工具统一命名为 `Cli_Toolbox.<tool_name>`。
- 业务需求层：
  - `[domain_1]`：
    - [列出该域专属命令、用途、入口。]
  - [若只有一个业务域，也必须显式独立成域，不得与抽象层混写。]
- 允许统一脚本入口。
- 抽象功能可共享；特定域命令禁止共享、禁止串用。
- 若声明工具，维护以下文档：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
- 若工具为多模块结构，维护以下开发索引：
  - `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - `references/tooling/development/modules/MODULE_TEMPLATE.md`
- 若技能存在运行态规则、约束、指引：
  - 必须提供 CLI 输出入口。
  - 必须提供 machine-readable `json/yaml` 合同。
  - markdown 只可作为审计版，不能作为模型运行时规则源。

## 3. 工作流约束
- 抽象层：
  - [写明抽象层工作流总则、统一入口、共通输入输出。]
- 业务需求层：
  - `[domain_1]`：
    - [写明该域流程步骤、输入输出和完成判定。]
  - [若存在多个业务域，继续逐域拆写；禁止混写。]

## 4. 规则约束
- 抽象层：
  - [写明顶层规则、边界、命名、门禁与禁止项。]
  - [若技能存在运行态规则，请显式声明：模型禁止直接阅读 markdown 获取运行指引；必须通过 CLI 读取 machine-readable 合同。]
  - [若技能存在运行态规则，请显式声明：规则必须同时存在 markdown 与 json/yaml 两份，更新时必须同步。]
- 业务需求层：
  - `[domain_1]`：
    - [写明该域的专属规则、专属边界、专属禁止项。]
  - [若存在多个业务域，继续逐域拆写；禁止混写。]

## 5. 方法论约束
- 抽象层：
  - [写明统一思维方式、统一推理方式、统一执行顺序。]
- 业务需求层：
  - `[domain_1]`：
    - [写明该域的专属方法论、专属例外条件。]
  - [若存在多个业务域，继续逐域拆写；禁止混写。]

## 6. 内联导航索引
- 抽象层：
  - [索引项 1] -> [相对路径]
  - [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
  - [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
  - [Cli_Toolbox 开发架构总览] -> [references/tooling/development/00_ARCHITECTURE_OVERVIEW.md]
  - [Cli_Toolbox 开发分类索引] -> [references/tooling/development/20_CATEGORY_INDEX.md]
  - [Cli_Toolbox 模块目录] -> [references/tooling/development/10_MODULE_CATALOG.yaml]
- 业务需求层：
  - `[domain_1]` -> [相对路径]
  - [若存在多个业务域，继续逐域列导航；禁止混写。]
- [若存在运行态规则：运行合同 JSON] -> [references/runtime/<CONTRACT>.json]
- [若存在运行态规则：运行合同审计版] -> [references/runtime/<CONTRACT>.md]

## 7. 架构契约
```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
├── references/
└── assets/
```
