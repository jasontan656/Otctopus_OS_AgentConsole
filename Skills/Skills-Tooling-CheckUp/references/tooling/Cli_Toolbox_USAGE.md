---
doc_id: "skills_tooling_checkup.tooling.toolbox_usage"
doc_type: "topic_atom"
topic: "Tooling entry contract for the local CLI-first runtime surface"
anchors:
  - target: "Cli_Toolbox_DEVELOPMENT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development templates should be maintained together."
  - target: "../governance/SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Generated tool docs should also respect doc-structure governance."
---

# Cli_Toolbox 使用文档

适用技能：`Skills-Tooling-CheckUp`

## 命名约束
- 本技能当前提供本地 `scripts/Cli_Toolbox.py`。
- 本地工具面固定为：
  - `Cli_Toolbox.contract`
  - `Cli_Toolbox.directive`

## 工具清单
- 运行时合同：
  - `python3 scripts/Cli_Toolbox.py contract --json`
- 运行时 directive：
  - `python3 scripts/Cli_Toolbox.py directive --topic <topic> --json`
- 实际进入目标 skill 后，仍复用：
  - 目标 skill 已存在的 CLI / scripts / tests / lint 命令
  - repo 已治理的 `*_skills` 环境
  - repo 已存在的治理技能命令

## 叙事式使用说明（固定格式）

### Cli_Toolbox.contract
- 人类叙事版输入：
  - “先给我这个技能的运行时合同，不要再让我沿 markdown 文件链去找规则。”
- 电脑动作发生了什么：
  - 读取 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`。
  - 直接把合同 payload 输出为 JSON。
- 人类叙事版输出：
  - 输出“先调用哪个命令、有哪些 directive topic、哪些边界是硬约束”。

### Cli_Toolbox.directive
- 人类叙事版输入：
  - “给我 read-audit / remediation / output-governance / techstack-baseline / tooling-entry 中某个 topic 的直接指令。”
- 电脑动作发生了什么：
  - 根据 `--topic` 查找同名 runtime contract JSON。
  - 直接输出该 topic 的 instruction / workflow / rules payload。
- 人类叙事版输出：
  - 输出“当前 topic 的直接行动指令、执行流程与硬规则”，而不是“下一步请继续读某个 markdown 文件”。

## 参数与结果（供 AI/工程使用）
- 输入：
  - `contract`：无额外参数
  - `directive`：`--topic <topic>`
- 输出：
  - `contract`：runtime 合同 payload
  - `directive`：topic 对应 payload
- 失败码约定：
  - `directive` 未知 topic 时返回 `unknown_directive_topic`

## 同步维护要求
- 修改 `scripts/Cli_Toolbox.py` 后，必须同步更新本文件、`Cli_Toolbox_DEVELOPMENT.md`、模块目录和对应文档。
- 新增 runtime-facing contract/workflow/instruction/guide 时，必须同时新增：
  - `*_human.md`
  - 同名 `.json`
- human mirror 的 Part B 必须与 CLI 输出使用的 JSON 保持一致。
