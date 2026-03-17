---
name: SkillsManager-Python-SubAgentGov
description: 把 Python subagent 并行治理主控沉淀为仓内正式技能，负责受管技能的发现、并发编排、证据落盘、串行 closeout 与断点恢复。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
  doc_structure:
    doc_id: skillsmanager_python_subagentgov.entry.facade
    doc_type: skill_facade
    topic: Entry facade for SkillsManager-Python-SubAgentGov
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the runtime contract.
    - target: ./references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The routing guide explains how to choose discovery, status, prompt render, or full governance.
---

# SkillsManager-Python-SubAgentGov

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py contract --json`
- Full governance entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py govern --json`
- 本技能是 `referenced + automation_cli + guardrailed` 的正式技能；`SKILL.md` 只做门面和路由，CLI JSON 是运行时主合同。

## 1. 技能定位
- 本技能把已经验证可运行的 Python subagent 并行治理主控产品化为仓内正式 skill。
- 本技能负责五类稳定职责：
  - 发现 `Skills/` 下受管目标技能
  - 为单技能启动外部 `codex exec --json` + `tmux` background subagent
  - 把每个 subagent 的 prompt、日志、结果和 closeout 证据落入 `Codex_Skill_Runtime`
  - 在主控内串行执行 `verify -> git traceability -> mirror sync -> session closeout`
  - 基于 runtime 证据执行断点恢复
- 本技能不负责：
  - 直接修改 `~/.codex/skills` 作为真源
  - 让单技能 subagent 自行做 commit、push 或 mirror
  - 在批量并行运行中隐式治理当前正在执行的主控自身；自治理必须显式指定单技能目标

## 2. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py contract --json`。
2. 再读取 `references/routing/TASK_ROUTING.md`，决定是看发现结果、runtime 状态、渲染 prompt 还是直接启动治理。
3. 再读取：
   - `references/policies/SKILL_EXECUTION_RULES.md`
   - `references/runtime_contracts/EXECUTION_BOUNDARY_DIRECTIVE_human.md`
   - `references/runtime_contracts/CLOSEOUT_SEQUENCE_DIRECTIVE_human.md`
4. 若要运行或维护 CLI，再进入 `references/tooling/`。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 规则层：
  - `references/policies/SKILL_EXECUTION_RULES.md`
- runtime 合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
  - `references/runtime_contracts/EXECUTION_BOUNDARY_DIRECTIVE_human.md`
  - `references/runtime_contracts/RUNTIME_LAYOUT_DIRECTIVE_human.md`
  - `references/runtime_contracts/CLOSEOUT_SEQUENCE_DIRECTIVE_human.md`
- tooling 层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：批量治理多个技能目录中的 Python 代码不规范问题，并且要求每个技能都保留独立 evidence / commit / mirror closeout。
- 适用于：需要保留并发 subagent 调度，但强制 closeout 串行执行的治理任务。
- 适用于：需要从 runtime 目录断点恢复、避免重复计算或 session 泄漏的技能治理任务。
- 不适用于：只想做一次性 ad-hoc 脚本运行且不需要 skill 级合同、文档和回归测试的场景。

## 5. 执行入口
- `contract`：读取 machine-readable runtime contract。
- `directive --topic <topic>`：读取固定治理指令。
- `list-targets`：发现受管技能并说明排除原因。
- `status`：汇总 runtime 目录中的 pending/active/completed 状态。
- `render-prompt --skill-name <name>`：为单技能渲染 subagent prompt 与结果文件落点。
- `govern`：启动或恢复整轮主控治理闭环。

## 6. 读取原则
- 始终以 repo 内 `Skills/` 为 truth source，`~/.codex/skills` 只通过 `SkillsManager-Mirror-To-Codex` 同步。
- 单技能 subagent 只修改一个技能目录，所有 Git 与 mirror 都由主控串行收口。
- 行为保持约束以 `Meta-refactor-behavior` 为前提；代码规范约束以 `Dev-PythonCode-Constitution` 为前提。
- 若要治理当前 skill 自身，必须显式指定 `--skill-name SkillsManager-Python-SubAgentGov`，不要在 all-scope 批处理里隐式自修改。

## 7. 结构索引
```text
SkillsManager-Python-SubAgentGov/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── prompt_template.md
├── references/
│   ├── policies/
│   ├── profiles/
│   ├── routing/
│   ├── runtime_contracts/
│   └── tooling/
├── scripts/
└── tests/
```
