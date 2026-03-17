---
doc_id: skillsmanager_python_subagentgov.references.runtime_contracts.skill_runtime_contract
doc_type: topic_atom
topic: Runtime contract for SkillsManager-Python-SubAgentGov
---

# Runtime Contract

## 技能角色
- `SkillsManager-Python-SubAgentGov` 是正式的 Python subagent 治理主控技能。
- 它把一次性 runtime 脚本沉淀为仓内可复用的 skill，并且保留以下关键行为：
  - 主控并发调度
  - 单技能 subagent 隔离
  - runtime evidence 落盘
  - 串行 verify / Git / mirror closeout
  - 断点恢复

## 固定执行面
- subagent 固定通过 `codex exec --json` 启动。
- subagent 固定由 `tmux` 守护。
- worker 模型固定为 `gpt-5.4`，`reasoning effort` 固定为 `high`。
- 默认最大并发为 `4`。

## 真源与镜像边界
- repo truth source 固定是 `Otctopus_OS_AgentConsole/Skills/`。
- `~/.codex/skills` 只允许通过 `SkillsManager-Mirror-To-Codex` 做同步安装。
- 单技能 subagent 不允许自己做 Git 或 mirror；这些动作由主控 closeout 串行完成。

## Runtime 证据
- controller 总状态写入：
  - `Codex_Skill_Runtime/SkillsManager-Python-SubAgentGov/controller_status.json`
- 每个技能的运行目录写入：
  - `prompt.md`
  - `codex.jsonl`
  - `last_message.txt`
  - `exit_code.txt`
  - `state.txt`
  - `result.json`
  - `result.md`
  - `closure.json`
  - `tmp/`

## 断点恢复
- 若 `closure.json` 已存在，该技能视为已完成 closeout。
- 若存在 `exit_code.txt`、`result.json` 或 tmux session，则视为需要恢复 closeout 或轮询中的 active 目标。
- controller 会在重新运行时从这些 runtime 证据恢复，而不是从头重复全部子任务。
