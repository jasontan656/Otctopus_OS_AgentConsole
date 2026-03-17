---
doc_id: skillsmanager_python_subagentgov.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for SkillsManager-Python-SubAgentGov
---

# Cli_Toolbox Usage

## 常用入口
- 读取合同：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py contract --json`
- 读取治理指令：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py directive --topic execution_boundary --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py directive --topic runtime_layout --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py directive --topic closeout_sequence --json`
- 发现目标技能：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py list-targets --json`
- 查看 runtime 状态：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py status --json`
- 渲染单技能 prompt：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py render-prompt --skill-name Meta-github-operation --json`
- 启动或恢复治理：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Python-SubAgentGov/scripts/Cli_Toolbox.py govern --json`

## 常用参数
- `--skill-name <name>`
  - 显式指定单个目标技能；可重复传入多个值。
- `--skills-root <path>`
  - 替换默认 `repo_root/Skills`，主要用于测试或受控演练。
- `--runtime-root <path>`
  - 替换默认 `Codex_Skill_Runtime/SkillsManager-Python-SubAgentGov`。
- `--include-self`
  - 仅影响 all-scope 发现；允许把当前技能自身纳入列表。
- `--max-parallel <1..4>`
  - 覆盖默认并发度，但上限仍受控为 4。
- `--poll-seconds <n>`
  - 覆盖轮询间隔，最小为 1 秒。

## 典型场景
- 先看哪些技能会被治理：
  - `list-targets --json`
- 检查一次中断任务是否可恢复：
  - `status --json`
- 只治理某一个技能：
  - `govern --skill-name Workflow-SiteMap-Creation --json`
- 显式治理当前技能自身：
  - `govern --skill-name SkillsManager-Python-SubAgentGov --json`
