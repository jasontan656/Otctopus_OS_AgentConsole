---
doc_id: "skill_creation_template.asset.toolbox_usage_template"
doc_type: "template_doc"
topic: "Template for a generated skill's Cli_Toolbox usage doc"
anchors:
  - target: "Cli_Toolbox_DEVELOPMENT_TEMPLATE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development templates should be maintained together."
  - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY_TEMPLATE.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Generated tool docs should also respect doc-structure governance."
---

# Cli_Toolbox 使用文档

适用技能：`${skill_name}`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- 抽象层：
  - [在此补充共享工具别名 -> 实际脚本路径]
- 业务需求层：
  - `[domain_1]`：
    - [在此补充该域专属工具别名 -> 实际脚本路径]
  - [若存在多个域，继续逐域列出；禁止混写。]
- 抽象功能可共享；特定域命令禁止共享、禁止串用。

## 叙事式使用说明（固定格式）

### <tool_alias>
- 人类叙事版输入：
  - [用自然语言写业务输入场景]
- 电脑动作发生了什么：
  - [写实际命令、参数、加载了哪些模板/脚本]
- 人类叙事版输出：
  - [写给老板/PM看得懂的结果解释，同时保留关键结构字段]

## 示例命令（强制）
- 最小用途描述：
  - [一句话描述该命令的最小用途]
- 一行命令（必须满足以下全部约束）：
  - 必须以 `cd <repo-root> &&` 开头。
  - 必须为“一行可复制”的完整命令。
  - 必须包含管道（例如 `| sed -n '1,200p'`）以便快速查看结果。
  - 命令必须能一键直达脚本预期参数并得到可复现输出。
- 示例：
  - `cd <repo-root> && ./.venv_backend_skills/bin/python Skills/${skill_name}/scripts/<tool_script>.py --arg-a "<value>" --arg-b "<value>" | sed -n '1,200p'`

## 参数与结果（供 AI/工程使用）
- 输入：
- 输出：
- 失败码约定：

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若为多模块 Toolbox，还需同步更新：
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档（`references/tooling/development/modules/*.md`）
- 若 skill 已采用 facade + routing + atomic docs 结构，还需同步更新：
  - `references/routing/`
  - `references/governance/`
- 若技能采用 staged CLI-first 复杂 profile，还应补齐：
  - `references/runtime/`
  - `references/stages/`
  - `assets/templates/stages/`
- 若工具承载运行态规则、约束、指引，还必须同步更新：
  - machine-readable 合同（`json/yaml`）
  - markdown 审计版
- 运行态规则默认应通过 CLI 输出；markdown 不应被写成模型直接读取的运行规则源。
