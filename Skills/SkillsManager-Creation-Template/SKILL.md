---
name: SkillsManager-Creation-Template
description: 提供受治理技能模板与统一 Cli_Toolbox，用于创建或改造 basic 与 staged_cli_first 技能。
metadata:
  doc_structure:
    doc_id: skillsmanager_creation_template.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Creation-Template skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# SkillsManager-Creation-Template

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 技能定位
- 本文件只做门面入口，不承载模板治理正文。
- 本技能负责把“创建新技能”和“治理既有技能”收敛为同一套受治理模板控制面。
- `basic` 与 `staged_cli_first` 都必须产出可路由、可继续治理的 skill 结构，而不是只生成一份大门面。

## 2. 必读顺序
1. 先读取 `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 再读取 `references/routing/TASK_ROUTING.md`，按任务意图分流。
3. 若任务涉及 profile 选择，再读取 `references/routing/PROFILE_ROUTING.md`。
4. 若任务涉及新建或治理 skill 结构，必须读取 `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`。
5. 真正动手前，再按分支进入 authoring contract、architecture playbook、staged profile reference 或 tooling docs。

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.json`
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.md`
- 路由层：
  - `references/routing/TASK_ROUTING.md`
  - `references/routing/PROFILE_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
  - `references/governance/SKILL_AUTHORING_RULES.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `references/governance/STAGED_PROFILE_REFERENCE.md`
- 资产与索引层：
  - `references/indexes/DOC_TREE.md`
  - `assets/skill_template/`
- 工具与验证层：
  - `scripts/Cli_Toolbox.py`
  - `scripts/create_skill_from_template.py`
  - `tests/test_create_skill_from_template_regression.py`

## 4. 适用域
- 适用于：创建新的受治理 skill 骨架。
- 适用于：治理既有 skill 的门面、routing、topic docs、contracts 与模板资产。
- 适用于：维护模板包、生成器、tooling docs 与回归闭环。
- 不适用于：直接代替目标 skill 编写其业务语义，或替代 mirror / git / installer 职责。

## 5. 执行入口
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py contract-reference --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py architecture-playbook --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py staged-skill-reference --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py skill-template --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py staged-skill-template --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract-template --json`
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py create-skill-from-template --skill-name <name> --target-root <path> --profile <basic|staged_cli_first> --overwrite`

## 6. 读取原则
- `SKILL.md` 只负责把读者送到下一层路由，不重新长回治理正文。
- 目标 skill 的入口门面 contract 由本技能定义；进入入口之后的文档树再交给 `SkillsManager-Doc-Structure` 治理。
- `SkillsManager-Doc-Structure` 是创建新 skill 与治理既有 skill 时必须显式应用的组成部分，不是隐式约定。
- 原有 `技能本体 / 规则说明` 双段式约定保留在原子治理文档与模板资产中，不再继续占满顶层门面。
- 若存在运行态规则，以 CLI 输出的 machine-readable contract 为准；markdown 只做人类审计与窄域导航。

## 7. 结构索引
```text
SkillsManager-Creation-Template/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   └── create_skill_from_template.py
├── assets/
│   └── skill_template/
├── references/
│   ├── governance/
│   ├── indexes/
│   ├── routing/
│   ├── runtime/
│   └── tooling/
└── tests/
    └── test_create_skill_from_template_regression.py
```
