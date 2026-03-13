---
name: "Workflow-OctopusOS-DevFlow"
description: "开发闭环 workflow 技能；当前先保持原骨架，后续再逐步通用化。"
---

# Workflow-OctopusOS-DevFlow

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 当前状态：暂时不启用，避免被误触发；仅在明确点名进行遗留查看、迁移或改造时使用。
- 本技能的唯一主轴是：`mother_doc -> construction_plan -> implementation -> acceptance`。
- 第一阶段先创建目录化项目说明骨架并回填；第二阶段把 mother doc 内的设计规划转成 AI 自用的 `Execution_atom_plan&validation_packs`；第三阶段按当前 active pack 施工并回填证据；第四阶段用真实 witness 做交付裁决，并在需要收口时把 `mother_doc` 顺序归档。
- 本技能不再绑定固定单项目目录；它按 `target_root + docs_root + codebase_root + graph_runtime_root` 解析当前任务载体。
- `target_root` 在本技能内表示 `AI_Projects` 内的 repo/workspace 根边界，不再默认等同代码对象根。
- `docs_root` 在本技能内表示当前代码对象唯一受管的开发文档根；后续所有 mother_doc、pack、graph、acceptance 都固定落在它下面。
- 目标项目根还必须位于 `AI_Projects` workspace 内；否则 `$Meta-RootFile-Manager` 无法收治目标模块 `AGENTS.md`，本技能必须拒绝服务。
- 目标代码对象的 `docs_root` 必须先存在；不存在时，本技能必须拒绝服务。
- 仅在项目结构初始化阶段，`Development_Docs/` 容器允许为空；一旦本技能介入具体开发闭环，`docs_root` 就必须已经是可用的真实目录。
- 开发文档的落盘容器必须先由 `Dev-OctopusOS-Constitution-ProjectStructure` 判定；若目标项目尚未固定其他特殊容器，则默认容器是 `<codebase_root>/Development_Docs/`，并且该目录本身就是当前 `docs_root`，不再额外要求 `<module_dir>` 物理子目录。
- 若目标模块下已经存在编号归档的 `NN_slug`，新一轮 `mother_doc` 不是空白起手；必须先从最近一轮归档与当前 code graph/context 抽取仍然有效的设计与增量，再开始回填。
- 若目标文件夹中已经存在 `execution_atom_plan_validation_packs/`、`pack_registry.yaml` 或既有 graph，必须先复用当前任务包与图谱上下文；禁止在同一目标上另起一条脱节的文档线。
- 目标模块的外部 `AGENTS.md` 必须由本技能模版创建，并由 `$Meta-RootFile-Manager` 收治；创建后必须立即执行 `collect`，使外部 `AGENTS.md` 与技能内治理映射形成闭环。
- 详细规则必须从下方入口文档读取，不得只凭本门面自行发挥。
- 默认路径解析：
  - `target_root`：当前 repo/workspace 根边界；默认取 `AI_Projects`
  - `docs_root`：当前代码对象唯一受管的开发文档根；默认是 `<codebase_root>/Development_Docs`
  - `development_docs_root`：与 `docs_root` 指向同一物理目录，仅作为 CLI/runtime 元数据保留
  - `module_dir`：可选逻辑主题标识，不参与物理路径拼接
  - `mother_doc_root`：`<docs_root>/mother_doc`
  - `construction_packs_root`：`<mother_doc_root>/execution_atom_plan_validation_packs`
  - `codebase_root`：默认 `<docs_root>/..`
  - `graph_runtime_root`：默认 `<docs_root>/graph`

## 2. 必读顺序
1. 顶层常驻文档只保留：
   - `rules/OCTOPUS_SKILL_HARD_RULES.md`
   - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
   - `/home/jasontan656/AI_Projects/AGENTS.md`
   - `<docs_root>/AGENTS.md`（若存在）
   - `/home/jasontan656/.codex/skills/Dev-OctopusOS-Constitution-ProjectStructure/SKILL.md`（当 `docs_root` 尚未固定时）
2. 进入任一阶段前，必须先读取目标位置预检：
   - `./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-runtime-contract --target-root <target_root> --docs-root <docs_root> [--development-docs-root <docs_root>] [--module-dir <logical_topic_id>] [--codebase-root <codebase_root>] [--graph-runtime-root <graph_runtime_root>] --json`
3. 进入任一阶段前，必须先读取：
   - `./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|construction_plan|implementation|acceptance> --target-root <target_root> --docs-root <docs_root> [--development-docs-root <docs_root>] [--module-dir <logical_topic_id>] --json`
4. 当前阶段的读物边界只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-doc-contract --stage <stage> --json`
5. 当前阶段的入口/门禁命令只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-command-contract --stage <stage> --json`
6. 当前阶段的 graph 角色只从工具取：
   - `./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-graph-contract --stage <stage> --json`
7. 阶段切换时，必须显式丢弃上一阶段的阶段文档与临时 focus，只保留第 `1` 步顶层常驻文档。
- 未完成 `1`、`2` 和 `3`，不得进入任何阶段执行。

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
  - `Skills/Meta-code-graph-base/SKILL.md`
  - `Skills/Meta-code-graph-base/scripts/meta_code_graph_base.py`
  - `Skills/Meta-RootFile-Manager/SKILL.md`
  - `Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py`
  - `/home/jasontan656/.codex/skills/Dev-OctopusOS-Constitution-ProjectStructure/SKILL.md`
- 运行边界层：
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `<docs_root>/AGENTS.md`（若存在）

## 4. 适用域
- 适用于：任何需要“开发文档驱动规划 -> 施工 -> evidence -> acceptance”闭环的软件开发任务。
- 适用于：后端、前端、CLI、服务编排、自动化脚本、运行时 bring-up，以及其他需要任务包和 graph 持续复用的开发位置。
- 不适用于：项目级结构治理本体；开发文档应落在哪里，应先由 `Dev-OctopusOS-Constitution-ProjectStructure` 判定。
- `Meta-code-graph-base` 负责生成与更新图谱；本技能只消费图谱产物和上下文。

## 5. 执行入口
- 任一阶段启动都固定先读：
  - `target-runtime-contract`
  - 必要时先执行 `target-scaffold`
  - `stage-checklist --stage <stage>`
  - `stage-doc-contract --stage <stage>`
  - `stage-command-contract --stage <stage>`
  - `stage-graph-contract --stage <stage>`
- 若本轮会改 mother_doc，模型应先判断需要改动的原子文档，再优先执行：
  - `mother-doc-mark-modified --path <mother_doc_root> --doc-ref <selected_doc>... --auto-from-git --json`
- `mother-doc-mark-modified` 的主语义是“模型显式给 doc_ref，Git diff/impact 自动兜底补齐”，不是完全放弃模型选择。
- 具体 init/lint/archive/graph 命令以 `stage-command-contract` 与 `stage-graph-contract` 输出为准。

## 6. 读取原则
- 门面只做“分类后的入口 + 适用域提示”。
- 顶层常驻文档只保留 `硬规则 + workflow contract + root AGENTS + project AGENTS + project-structure skill（当 docs_root 未固定时）`。
- `Meta-code-graph-base` 只按 `stage-graph-contract` 读取或更新，不属于顶层常驻文档。
- `$Meta-RootFile-Manager` 负责把目标模块 `AGENTS.md` 收治进治理映射模版；本技能必须通过它完成 `AGENTS` 闭环，而不是自行绕开治理链。
- 进入任何阶段前，必须先做目标位置预检，确认当前任务是“复用已有 mother_doc / task pack / graph”还是“创建新骨架”。
- 若模块容器已具备使用条件但缺少 `AGENTS.md`、mother doc、task packs 或 graph，必须先执行 `target-scaffold` 一次性补齐骨架。
- 当 mother_doc 已发生真实修改时，优先由模型显式选择应回到 `modified` 的原子文档，再用 `mother-doc-mark-modified --auto-from-git` 做 Git diff / impact 兜底检查。
- 若当前目标已经存在任务包、归档轮次或图谱，必须沿用当前脉络继续开发，不得另起一套脱节的说明书。
- 单阶段执行时，只读当前阶段 checklist 与当前阶段直接需要的模板/文档；禁止展开其他阶段规范。
- 多阶段连续执行时，阶段切换后必须重新读取当前阶段 checklist，并丢弃上一阶段阶段文档、checklist 与 instruction focus。
- 用户若以问答方式回填 mother doc，回复应提供结构化选项或有界提示，不得散讲成长文。
- 规则正文、阶段语义、字段要求、lint 口径、模板结构一律以下沉文档为准。
- 需要什么读什么，不得把所有引用文档一次性展开成新的门面正文。

## 7. 结构索引
```text
Workflow-OctopusOS-DevFlow/
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
