---
name: Workflow-CentralFlow1-OctopusOS
description: 开发闭环 workflow 技能；当前先保持原骨架，后续再逐步通用化。
metadata:
  doc_structure:
    doc_id: workflow_centralflow1_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-CentralFlow1-OctopusOS skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Workflow-CentralFlow1-OctopusOS

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow1-OctopusOS/scripts/Cli_Toolbox.py workflow-contract --json`
- Target runtime entry: `./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow1-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --target-root <target_root> --docs-root <docs_root> --json`
- Stage checklist entry: `./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow1-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|construction_plan|implementation|acceptance> --target-root <target_root> --docs-root <docs_root> --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.

## 1. 技能定位
- 本文件只做门面入口，不承载规则正文。
- 本技能负责把开发任务收敛到统一闭环：`mother_doc -> construction_plan -> implementation -> acceptance`。
- 详细规则、阶段门禁、字段要求、lint 口径与执行细节全部后置到 `rules/`、`references/` 与 `scripts/Cli_Toolbox.py`。

## 2. 入口分流
- 总体运行合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
  - `scripts/Cli_Toolbox.py workflow-contract --json`
- 目标位置与阶段预检：
  - `scripts/Cli_Toolbox.py target-runtime-contract --json`
  - `scripts/Cli_Toolbox.py stage-checklist --stage <stage> --json`
- 阶段读物、命令与 graph 入口：
  - `scripts/Cli_Toolbox.py stage-doc-contract --stage <stage> --json`
  - `scripts/Cli_Toolbox.py stage-command-contract --stage <stage> --json`
  - `scripts/Cli_Toolbox.py stage-graph-contract --stage <stage> --json`
- 硬规则入口：
  - `rules/OCTOPUS_SKILL_HARD_RULES.md`
- 工作流入口：
  - `references/tooling/SKILL_TOOLING_EXECUTION_PLAYBOOK.md`
- 模板入口：
  - `assets/templates/mother_doc/`
  - `assets/templates/execution_atom_plan_validation_packs/`
  - `assets/templates/REQUIREMENT_ATOM_TEMPLATE.md`
  - `assets/templates/ACCEPTANCE_REPORT_TEMPLATE.md`
  - `assets/templates/ACCEPTANCE_MATRIX_TEMPLATE.md`

## 3. 最小读取顺序
1. 先读取 `workflow-contract --json`。
2. 再读取 `target-runtime-contract --json`，确认当前 `target_root / docs_root / codebase_root / graph_runtime_root`。
3. 进入具体阶段前，读取 `stage-checklist --stage <stage> --json`。
4. 只有在当前阶段需要时，再读取对应的 `stage-doc-contract / stage-command-contract / stage-graph-contract`，以及 `rules/`、`references/tooling/`、模板资产。

## 4. 适用域
- 适用于：需要用开发文档驱动规划、施工、证据回填与验收收口的软件开发任务。
- 适用于：需要 `mother_doc`、`execution_atom_plan_validation_packs`、acceptance artifacts 与 graph context 协同工作的任务。
- 不适用于：项目级结构治理本体；开发文档容器与模块落位应先由 `Dev-ProjectStructure-Constitution` 判定。

## 5. 读取原则
- 门面只负责路由，不重复展开规则正文。
- 需要什么读什么；不要把阶段规则、模板细则或执行约束重新堆回 `SKILL.md`。
- 若任务进入具体阶段，以 CLI 输出和下沉文档为准，不以门面页自行补规则。

## 6. 结构索引
```text
Workflow-CentralFlow1-OctopusOS/
├── SKILL.md
├── rules/
│   └── OCTOPUS_SKILL_HARD_RULES.md
├── references/
│   ├── runtime_contracts/
│   └── tooling/
├── assets/
│   └── templates/
├── scripts/
│   └── Cli_Toolbox.py
└── agents/
    └── openai.yaml
```
