---
name: SkillsManager-Creation-Template
description: 提供技能脚手架 profile、生成策略与受治理 CLI，用于创建符合工程化技能标准的新技能骨架。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
  doc_structure:
    doc_id: skillsmanager_creation_template.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Creation-Template skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
    - target: ./references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: Routing guidance selects the correct scaffold profile before generation.
---

# SkillsManager-Creation-Template

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py contract --json`
- Profile catalog entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py profile --json`
- Scaffold execution entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py scaffold --skill-name <name> --target-root <dir> --doc-topology <profile> --tooling-surface <profile> --workflow-control <profile>`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.

## 1. 技能定位
- 本文件只做门面入口，不承载模板正文。
- 本技能只负责三件事：
  - 定义稳定的技能 profile 语义
  - 维护脚手架模板资产与生成编排
  - 让新技能从一开始就落到 `facade + references + scripts + tests` 的工程化形态
- 本技能不再把 `guide_only / guide_with_tool / executable_workflow_skill` 当作长期标准。
- 模板决策改为三条正交轴：
  - `doc_topology`
  - `tooling_surface`
  - `workflow_control`

## 2. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py contract --json`。
2. 再执行 `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py profile --json`，确认允许的 profile 组合。
3. 若要判断该选哪类脚手架，再读取 `references/routing/TASK_ROUTING.md`。
4. 若要理解 profile 语义与约束，再读取：
   - `references/profiles/SKILL_PROFILE_SCHEMA.md`
   - `references/policies/SCAFFOLD_POLICY.md`
5. 若要真的落盘生成，再进入 `references/tooling/` 查看 CLI usage/development 文档。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- profile 层：
  - `references/profiles/SKILL_PROFILE_SCHEMA.md`
  - `references/profiles/TEMPLATE_CATALOG.md`
- 策略层：
  - `references/policies/SCAFFOLD_POLICY.md`
- runtime 合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
- tooling 层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：创建新技能、把旧技能重构为稳定 profile、统一技能脚手架目录与 runtime 合同。
- 适用于：需要同时决定文档拓扑、CLI 能力面与 workflow 控制级别的技能创建任务。
- 不适用于：替代具体技能的业务方法论，或把 repo-local 命令名硬编码成长期标准。

## 5. 执行入口
- `contract`：读取 machine-readable runtime contract。
- `directive --topic <topic>`：读取固定治理指令。
- `profile`：查看支持的 profile 组合与默认推荐。
- `scaffold`：按最终 profile 直接生成目标技能骨架。

## 6. 读取原则
- 门面只负责路由，不重新长回模板正文。
- 稳定的是 profile 语义与 contract schema，不是旧模板名。
- `workflow_path` 仍然是正式 profile，但不是默认真理。
- 若 profile 不需要 `path/`、`scripts/` 或 `tests/`，不应为照顾旧习惯强行生成。

## 7. 结构索引
```text
SkillsManager-Creation-Template/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── policies/
│   ├── profiles/
│   ├── routing/
│   ├── runtime_contracts/
│   └── tooling/
├── scripts/
└── tests/
```
