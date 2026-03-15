---
doc_id: skills_tooling_checkup.tooling.toolbox_usage
doc_type: topic_atom
topic: Tooling entry contract for the local CLI-first runtime surface
---

# Cli_Toolbox 使用文档

适用技能：`SkillsManager-Tooling-CheckUp`

## 命名约束
- 本技能当前提供本地 `scripts/Cli_Toolbox.py`。
- 本地工具面固定为：
  - `Cli_Toolbox.contract`
  - `Cli_Toolbox.directive`
  - `Cli_Toolbox.govern_target`

## 工具清单
- 运行时合同：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`
- 运行时 directive：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic <topic> --json`
- 目标技能 tooling surface 审计入口：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
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

### Cli_Toolbox.govern_target
- 人类叙事版输入：
  - “拿这个技能去审计另一个 skill 的 tooling surface，告诉我它现在哪里不合规。”
- 电脑动作发生了什么：
  - 读取目标 skill root。
  - 对照本技能内置的 tooling-entry contract，检查 CLI 入口、runtime_contracts、human/json 配对、SKILL.md facade、`agents/openai.yaml`。
  - 直接输出目标感知的治理审计 JSON。
- 人类叙事版输出：
  - 输出“目标 skill 当前是否存在受管 tooling surface、缺了哪些双文件配对、哪些 legacy runtime docs 还在 markdown-only、下一步该改什么”。

## 参数与结果（供 AI/工程使用）
- 输入：
  - `contract`：无额外参数
  - `directive`：`--topic <topic>`
  - `govern-target`：`--target-skill-root <path>`
- 输出：
  - `contract`：runtime 合同 payload
  - `directive`：topic 对应 payload
  - `govern-target`：目标 skill tooling surface 审计结果
- 失败码约定：
  - `directive` 未知 topic 时返回 `unknown_directive_topic`
  - `govern-target` 找不到 skill root 或缺失 `SKILL.md` 时返回对应错误

## 同步维护要求
- 修改 `scripts/Cli_Toolbox.py` 后，必须同步更新本文件、`Cli_Toolbox_DEVELOPMENT.md`、模块目录和对应文档。
- 新增 runtime-facing contract/workflow/instruction/guide 时，必须同时新增：
  - `*_human.md`
  - 同名 `.json`
- human mirror 的 Part B 必须与 CLI 输出使用的 JSON 保持一致。
