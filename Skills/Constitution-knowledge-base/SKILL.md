---
name: "Constitution-knowledge-base"
description: 宪法库技能用于让大模型使用关键字查询,相关规范并遵守（基线入口：assets/goal/MOL_FULL_CANON.md；工具入口：Cli_Toolbox.constitution_keyword_query）
---

# Constitution-knowledge-base

## 1. 目标
- 基线文档：`assets/goal/MOL_FULL_CANON.md`（宪法技能唯一基线；一切宪法内容由其衍生）。
- 把宪法库作为 AI 可检索约束源，采用“人类版 Markdown + 机器版 JSONL”双轨结构。
- 当前只提供一类能力：
  - 双语关键词查询并输出机械约束规则（JSONL）。
- 当前查询面只保留仍由宪法库自身治理的 `constraints` 命中结果；已被外部技能接管的结构、前端、Python 规则不再作为本技能查询底座。
- 执行合同仅描述查询输出应携带的命中约束与执行边界，不再承载 Python 代码 lint、前端规范、项目结构规则与胖文件治理。

## 2. 可用工具（可选填充，条目必须存在）
- `Cli_Toolbox.constitution_keyword_query`
  - 入口：`scripts/constitution_keyword_query.py`
  - 职责：单一查询工具；接收双语关键词参数，只输出真实命中的 `constraints` 机器规则。
  - 输出：仅打印到 console，且仅允许 `JSONL` 机械输出（含 `id/cat/domain/src/must/forbid/gate`）；禁止 markdown 人类文本输出与落盘参数。

## 3. 工作流约束
- 查询步骤（强制）：
  1. 先准备双语关键词：中文放入 `--keywords-zh`，英文放入 `--keywords-en`。
  2. 直接运行查询命令：`./.venv_backend_skills/bin/python Skills/Constitution-knowledge-base/scripts/constitution_keyword_query.py --keywords-zh "<zh_terms>" --keywords-en "<en_terms>"`。
  3. 将控制台返回的 JSONL 逐行作为机器规则消费：识别 `query_meta`、`constitution_rule`、`no_hit` 三类记录。
  4. 将 `minimum_keyword_contract` 作为输入门槛合同：若双语关键词不足最小门槛，必须阻断并补词后重跑。
  5. 将 `constitution_enforcement_contract` 作为强执行合同：读取 `required_common_anchors/required_constraint_anchors/required_gates/static_enforcement_scope`；当前 `required_common_anchors` 与 `required_constraint_anchors` 默认为空集合。
- 输出与执行边界（强制）：
  - 查询工具仅允许控制台输出，禁止任何落盘参数。
  - 查询工具仅允许机械 `JSONL`，禁止 markdown 人类正文输出。
  - 宪法查询命令禁止限行输出：禁止 `sed -n/head/tail/awk 'NR...'` 截断结果。

## 4. 规则约束
- 查询输出记录类型（强制）：
  - `query_meta`
  - `minimum_keyword_contract`
  - `constitution_rule`
  - `no_hit`
  - `constitution_enforcement_contract`
- 机器规则对象字段（强制）：
  - `id/cat/domain/priority/cohit/title_en/keywords_en/keywords_zh/must/forbid/gate/evidence/src`
- 分组合同（强制）：
  - `common_core`：保留为空分组兼容位，不再承载已迁出的规则。
  - `common_conditional`：保留为空分组兼容位，不再承载已迁出的规则。
  - `constraints`：仅在命中时输出。
- lint gate 范围（强制）：
  - Python 代码 lint、胖文件检查、类型契约/权限边界/payload normalize 等 Python 静态 gate 已迁出本技能，由 `Dev-PythonCode-Constitution` 单独承接。
  - 前端组件、布局、动效、showroom/workbench 相关规范已迁出本技能，由 `Dev-VUE3-WebUI-Frontend` 单独承接。
  - 项目级目录、容器、结构、模块定位与热插拔边界已迁出本技能，由 `Dev-OctopusOS-Constitution-ProjectStructure` 单独承接。
  - 宪法库不再提供本地 lint CLI。

## 5. 方法论约束
- `machine-first`：查询输出面向 AI 机器消费，避免人类叙事噪音。
- `compact-first`：字段极简、结构固定、稳定可拼接。
- `deterministic-order`：命中项按 `score desc + id asc` 排序。
- `traceable-source`：每条机器规则必须携带 `src` 绝对路径。
- `query-only-after-migration`：结构、前端、Python 静态治理职责迁出后，宪法库只保留未外移的查询职责。

## 6. 内联导航索引
- 技能说明：`SKILL.md`
- 宪法基线入口：`assets/goal/MOL_FULL_CANON.md`
- 查询工具入口：`scripts/constitution_keyword_query.py`
- 机器语料构建脚本：`scripts/build_machine_anchor_docs.py`
- MOL 关键词锚点图（v1）：`references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- 锚点文档注册表：`references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml`
- 机器语料（JSONL）：`references/anchor_docs_machine/anchor_docs_machine_v1.jsonl`
- Cli_Toolbox 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
- Cli_Toolbox 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 7. 架构契约
```text
Constitution-knowledge-base/
├── SKILL.md
├── scripts/
│   ├── constitution_keyword_query.py
│   ├── build_machine_anchor_docs.py
│   └── ckb_toolbox/
├── assets/
│   └── goal/
│       └── MOL_FULL_CANON.md
└── references/
    ├── anchor_docs/
    ├── anchor_docs_machine/
    ├── governance/
    ├── knowledge_graph/
    └── tooling/
```

落地规则：
- `1-7` 章节必须完整保留。
- 查询工具输出以机器 JSONL 为唯一对外合同；Markdown 仅作为人类阅读资产。
- Python lint 与胖文件治理已迁移到 `Dev-PythonCode-Constitution`；前端规范已迁移到 `Dev-VUE3-WebUI-Frontend`；项目结构规则已迁移到 `Dev-OctopusOS-Constitution-ProjectStructure`；本技能不再内置 lint 工具。
