---
name: SkillsManager-Tooling-CheckUp
description: 治理技能的 machine contract、runtime/tooling surface、artifact policy 与 remediation gate，并以 contract-first 方式执行审计。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
  doc_structure:
    doc_id: skillsmanager_tooling_checkup.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Tooling-CheckUp skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
    - target: ./references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The routing guide explains how contract-first tooling audits work.
---

# SkillsManager-Tooling-CheckUp

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`
- Audit entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py audit --target-skill-root <path> --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.

## 1. 技能定位
- 本技能只治理 target skill 的 runtime/tooling 合同，不再把旧路径偏好、旧命令名或绝对输出目录写成长期标准。
- 当前稳定职责只有四类：
  - machine contract 审计
  - runtime/tooling surface 探测
  - artifact policy 检查
  - remediation gate 生成
- 本技能不治理 target skill 的根目录拓扑；那属于 `SkillsManager-Doc-Structure`。

## 2. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`。
2. 再按任务进入：
   - `references/routing/TASK_ROUTING.md`
   - `references/profiles/TOOLING_SURFACE_PROFILES.md`
3. 若要理解审计边界，再读取：
   - `references/policies/CONTRACT_AUDIT_POLICY.md`
   - `references/policies/ARTIFACT_POLICY.md`
   - `references/policies/PYTHON_TOOLING_BOUNDARY.md`
   - `references/policies/REMEDIATION_GATE.md`
4. 若要运行或维护 CLI，再进入 `references/tooling/`。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- profile 层：
  - `references/profiles/TOOLING_SURFACE_PROFILES.md`
- 规则层：
  - `references/policies/CONTRACT_AUDIT_POLICY.md`
  - `references/policies/ARTIFACT_POLICY.md`
  - `references/policies/PYTHON_TOOLING_BOUNDARY.md`
  - `references/policies/REMEDIATION_GATE.md`
- runtime 合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
- tooling 层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：技能 contract 校验、CLI surface 审计、artifact policy 审计、tooling 文档/测试闭环检查。
- 适用于：需要判断 target skill 是否符合 `none / contract_cli / automation_cli` 三类能力面的场景。
- 不适用于：替代 Python 语言 lint、替代结构拓扑 lint、替代业务语义评审。

## 5. 执行入口
- `contract`：读取 machine-readable runtime contract。
- `directive --topic <topic>`：读取固定治理指令。
- `audit`：对 target skill 执行 contract-first 审计。

## 6. 读取原则
- 优先看 contract schema 与 artifact policy，而不是旧 `Cli_Toolbox.py + read-contract-context` 组合。
- repo-local 路径规则应由 resolver/integration contract 提供，不应写死到技能门面里。
- remediation gate 只产出整改方向，不直接改 target skill。

## 7. 结构索引
```text
SkillsManager-Tooling-CheckUp/
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
