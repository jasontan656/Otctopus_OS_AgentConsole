---
name: "Disabled-Octupos-OS-Backend"
description: "暂时不启用，避免被误触发；仅保留为可修改的历史章鱼后端技能。"
---

# Disabled-Octupos-OS-Backend

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 当前状态：暂时不启用，避免被误触发；仅在明确点名进行遗留查看、迁移或改造时使用。
- 本技能的唯一主轴是：`mother_doc -> construction_plan -> implementation -> acceptance`。
- 第一阶段先创建目录化项目说明骨架并回填；第二阶段把 mother doc 内的设计规划转成 AI 自用的 `Execution_atom_plan&validation_packs`；第三阶段按当前 active pack 施工并回填证据；第四阶段用真实 witness 做交付裁决，并在需要收口时把 `mother_doc` 顺序归档。
- 若 `docs/` 下已经存在编号归档的 `NN_slug`，新一轮 `mother_doc` 不是空白起手；必须先从最近一轮归档与当前 code graph/context 抽取仍然有效的设计与增量，再开始回填。
- 详细规则必须从下方入口文档读取，不得只凭本门面自行发挥。
- root-first 路径：
  - mother doc root：`<root>/OctuposOS_Runtime_Backend/docs/mother_doc`
  - mother doc index：`<root>/OctuposOS_Runtime_Backend/docs/mother_doc/00_index.md`
  - construction packs root：`<root>/OctuposOS_Runtime_Backend/docs/mother_doc/execution_atom_plan_validation_packs`
  - construction packs index：`<root>/OctuposOS_Runtime_Backend/docs/mother_doc/execution_atom_plan_validation_packs/00_index.md`
  - runtime：`<root>/OctuposOS_Runtime_Backend`
  - codebase：`<root>/Octopus_CodeBase_Backend`

## 2. 必读顺序
1. 顶层常驻文档只保留：
   - `rules/OCTOPUS_SKILL_HARD_RULES.md`
   - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
   - `<root>/AGENTS.md`
   - `<root>/Octopus_CodeBase_Backend/AGENTS.md`
2. 进入任一阶段前，必须先读取：
   - `./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|construction_plan|implementation|acceptance> --json`
3. 当前阶段的读物边界只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py stage-doc-contract --stage <stage> --json`
4. 当前阶段的入口/门禁命令只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py stage-command-contract --stage <stage> --json`
5. 当前阶段的 graph 角色只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py stage-graph-contract --stage <stage> --json`
6. 阶段切换时，必须显式丢弃上一阶段的阶段文档与临时 focus，只保留第 `1` 步顶层常驻文档。
- 未完成 `1` 和 `2`，不得进入任何阶段执行。

## 3. 分类入口
- 规则层：
  - `rules/OCTOPUS_SKILL_HARD_RULES.md`
- 工作流层：
  - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- 模板层：
  - `assets/templates/mother_doc/*`
  - `assets/templates/execution_atom_plan_validation_packs/*`
  - `assets/templates/REQUIREMENT_ATOM_TEMPLATE.md`
  - `assets/templates/ACCEPTANCE_REPORT_TEMPLATE.md`
  - `assets/templates/ACCEPTANCE_MATRIX_TEMPLATE.md`
- 工具层：
  - `scripts/Cli_Toolbox.py`
- 外部辅助层：
  - `<root>/Otctopus_OS_AgentConsole/Skills/Meta-code-graph-base/SKILL.md`
  - `<root>/Otctopus_OS_AgentConsole/Skills/Meta-code-graph-base/scripts/meta_code_graph_base.py`
- 运行边界层：
  - `<root>/AGENTS.md`
  - `<root>/Octopus_CodeBase_Backend/AGENTS.md`

## 4. 适用域
- 适用于：后端项目说明驱动的规划、施工、验收闭环。
- 不适用于：前端设计、浏览器自动化、图谱生成本体、多仓全域 discovery。
- `Meta-code-graph-base` 负责生成与更新图谱；本技能只消费图谱产物和上下文。

## 5. 执行入口
- 任一阶段启动都固定先读：
  - `stage-checklist --stage <stage>`
  - `stage-doc-contract --stage <stage>`
  - `stage-command-contract --stage <stage>`
  - `stage-graph-contract --stage <stage>`
- 具体 init/lint/archive/graph 命令以 `stage-command-contract` 与 `stage-graph-contract` 输出为准。

## 6. 读取原则
- 门面只做“分类后的入口 + 适用域提示”。
- 顶层常驻文档只保留 `硬规则 + workflow contract + root AGENTS + companion AGENTS`。
- `Meta-code-graph-base` 只按 `stage-graph-contract` 读取或更新，不属于顶层常驻文档。
- 单阶段执行时，只读当前阶段 checklist 与当前阶段直接需要的模板/文档；禁止展开其他阶段规范。
- 多阶段连续执行时，阶段切换后必须重新读取当前阶段 checklist，并丢弃上一阶段阶段文档、checklist 与 instruction focus。
- 用户若以问答方式回填 mother doc，回复应提供结构化选项或有界提示，不得散讲成长文。
- 规则正文、阶段语义、字段要求、lint 口径、模板结构一律以下沉文档为准。
- 需要什么读什么，不得把所有引用文档一次性展开成新的门面正文。

## 7. 结构索引
```text
Disabled-Octupos-OS-Backend/
├── SKILL.md
├── rules/
│   └── OCTOPUS_SKILL_HARD_RULES.md
├── references/
│   └── tooling/
│       └── SKILL_TOOLING_WORKFLOW_CONTRACT.md
├── assets/
│   └── templates/
├── scripts/
│   └── Cli_Toolbox.py
└── agents/
    └── openai.yaml
```
