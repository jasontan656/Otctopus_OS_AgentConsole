---
doc_id: functional_humenworkzone_manager.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: Usage guide for the Functional-HumenWorkZone-Manager CLI toolbox
anchors:
- target: Cli_Toolbox_DEVELOPMENT.md
  relation: pairs_with
  direction: lateral
  reason: Usage and development docs should stay aligned.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: governed_by
  direction: downstream
  reason: Toolbox docs must respect doc-structure governance.
---

# Cli_Toolbox 使用文档

适用技能：`Functional-HumenWorkZone-Manager`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- `Cli_Toolbox.contract`
  - 作用：输出本技能的 CLI-first runtime contract。
- `Cli_Toolbox.directive`
  - 作用：按 topic 输出 runtime guide/contract，当前支持 `task-routing` 与 `execution-boundary`。
- `Cli_Toolbox.paths`
  - 作用：输出 `Human_Work_Zone` 根路径与各受管子区的 canonical 路径。

## 示例命令（强制）
- 最小用途描述：
  - 读取 skill runtime contract
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole && ./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json | sed -n '1,200p'`
- 最小用途描述：
  - 读取任务分流 guide
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole && ./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic task-routing --json | sed -n '1,220p'`
- 最小用途描述：
  - 读取执行边界 contract
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole && ./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json | sed -n '1,220p'`
- 最小用途描述：
  - 查看受管目录与各子区路径
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole && ./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json | sed -n '1,200p'`

## 参数与结果（供 AI/工程使用）
- 输入：
  - `contract`：无额外参数，可选 `--json`
  - `directive`：`--topic <task-routing|execution-boundary>`，可选 `--json`
  - `paths`：无额外参数，可选 `--json`
- 输出：
  - `contract`：runtime contract payload
  - `directive`：指定 topic 的 directive payload
  - `paths`：`Human_Work_Zone` 根与各受管子区路径
- 失败码约定：
  - 未知 topic：非零退出，并输出可用 topic 列表

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若 CLI 输出形态或 topic 集合变化，必须同步更新：
  - `references/runtime_contracts/*.json`
  - `references/runtime_contracts/*_human.md`
  - `SKILL.md`
  - `agents/openai.yaml`
- 运行态规则默认应通过 CLI 输出；markdown 不应被写成模型直接读取的运行规则源。
