---
name: SkillsManager-Doc-Structure
description: 治理技能的门面、references 与 workflow_path 文档拓扑，并以 profile-aware 方式执行结构 lint 与上下文编译。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
  doc_structure:
    doc_id: skillsmanager_doc_structure.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Doc-Structure skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
    - target: ./references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The routing guide explains how topology-aware linting works.
---

# SkillsManager-Doc-Structure

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`
- Lint entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py lint --target <skill_root> --json`
- Compile entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py compile-context --target <skill_root> --entry <entry> --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.

## 1. 技能定位
- 本技能只负责文档拓扑治理，不再把家族模板目录形态当作长期标准。
- 当前稳定职责只有三类：
  - 判定 target skill 的 `doc_topology`
  - 校验门面、references 与 workflow_path 的结构边界
  - 按 profile 编译最小必要上下文
- 本技能不治理 target skill 的业务语义、repo-local 输出路径或 Python 语言风格细节。

## 2. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`。
2. 再根据任务进入：
   - `references/routing/TASK_ROUTING.md`
   - `references/profiles/DOC_TOPOLOGY_PROFILES.md`
3. 若要理解 lint 规则，再读取：
   - `references/policies/FACADE_POLICY.md`
   - `references/policies/REFERENCE_GRAPH_POLICY.md`
   - `references/policies/WORKFLOW_PATH_POLICY.md`
4. 若要运行或维护 CLI，再进入 `references/tooling/`。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- profile 层：
  - `references/profiles/DOC_TOPOLOGY_PROFILES.md`
- 规则层：
  - `references/policies/FACADE_POLICY.md`
  - `references/policies/REFERENCE_GRAPH_POLICY.md`
  - `references/policies/WORKFLOW_PATH_POLICY.md`
- runtime 合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
- tooling 层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：技能门面重构、references 结构治理、workflow_path 编排治理、reading-chain 编译检查。
- 适用于：需要同时支持 `inline`、`referenced`、`workflow_path` 三类技能的结构 lint。
- 不适用于：替代具体技能的方法论正文，也不替代 `SkillsManager-Tooling-CheckUp` 的 CLI/tooling 审计。

## 5. 执行入口
- `contract`：读取 machine-readable runtime contract。
- `directive --topic <topic>`：读取结构治理固定指令。
- `inspect`：判定目标技能的 profile 与可用上下文入口。
- `lint`：执行结构治理检查。
- `compile-context`：按当前 profile 编译最小上下文。

## 6. 读取原则
- 稳定的是 profile-aware 结构规则，不是旧的 `skill_mode -> shape` 映射。
- `references/` 与 `workflow_path` 都是正式形态。
- 若技能本身不需要 `path/`，不要被旧家族习惯强行拉回 `path-first`。

## 7. 结构索引
```text
SkillsManager-Doc-Structure/
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
