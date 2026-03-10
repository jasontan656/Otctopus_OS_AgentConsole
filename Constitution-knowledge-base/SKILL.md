---
name: "Constitution-knowledge-base"
description: 宪法库技能用于让大模型使用关键字查询,相关规范并遵守（基线入口：assets/goal/MOL_FULL_CANON.md；工具入口：Cli_Toolbox.constitution_keyword_query）
---

# Constitution-knowledge-base

## 1. 目标
- 基线文档：`assets/goal/MOL_FULL_CANON.md`（宪法技能唯一基线；一切宪法内容由其衍生）。
- 把宪法库作为 AI 可检索约束源，采用“人类版 Markdown + 机器版 JSONL”双轨结构。
- 当前提供两类能力：
  - 双语关键词查询并输出机械规则（JSONL）。
  - 静态 lint gate：仅覆盖可被静态验证的结构、契约与边界条款。
- 固化“common_core 始终附带 + common_conditional/constraints 按命中输出”的查询合同语义。
- 执行门禁合同只保留可静态验证的 gate，不承载运行态证据、技术栈选型或依赖绑定。

## 2. 可用工具（可选填充，条目必须存在）
- `Cli_Toolbox.constitution_keyword_query`
  - 入口：`scripts/constitution_keyword_query.py`
  - 职责：单一查询工具；接收双语关键词参数，按关联命中 `common_conditional/constraints`，并始终输出完整 `common_core` 机器规则。
  - 输出：仅打印到 console，且仅允许 `JSONL` 机械输出（含 `id/cat/domain/src/must/forbid/gate`）；禁止 markdown 人类文本输出与落盘参数。
- `Cli_Toolbox.run_constitution_lints`
  - 入口：`scripts/run_constitution_lints.py`
  - 职责：对目标代码库执行静态 lint gate，覆盖 `code_governance/fat_file/file_structure/folder_structure/modularity/typed_contract/payload_normalize/permission_boundary/hardcoded_asset/absolute_path`。
  - 输出：仅打印 JSON，失败返回非零退出码。

## 3. 工作流约束
- 查询步骤（强制）：
  1. 先准备双语关键词：中文放入 `--keywords-zh`，英文放入 `--keywords-en`。
  2. 直接运行查询命令：`python3 scripts/constitution_keyword_query.py --keywords-zh "<zh_terms>" --keywords-en "<en_terms>"`。
  3. 将控制台返回的 JSONL 逐行作为机器规则消费：识别 `query_meta`、`constitution_rule`、`no_hit` 三类记录。
  4. 将 `minimum_keyword_contract` 作为输入门槛合同：若双语关键词不足最小门槛，必须阻断并补词后重跑。
  5. 将 `constitution_enforcement_contract` 作为强执行合同：读取 `required_common_anchors/required_constraint_anchors/required_gates/static_enforcement_scope`。
- lint 步骤（强制）：
  1. 保留条款若要作为 gate 生效，必须有对应静态 lint 模块。
  2. 对目标仓库运行：`python3 scripts/run_constitution_lints.py --target <repo_root>`。
  3. 任何 `status=fail` 都必须阻断，不允许人工口头放行。
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
  - `common_core`：始终全量输出。
  - `common_conditional/constraints`：仅在命中时输出。
- lint gate 范围（强制）：
  - 只覆盖可静态验证条款。
  - 运行态证据、发布门禁、回滚演练、技术栈绑定不得继续保留为宪法 gate。

## 5. 方法论约束
- `machine-first`：查询输出面向 AI 机器消费，避免人类叙事噪音。
- `compact-first`：字段极简、结构固定、稳定可拼接。
- `deterministic-order`：`common_core` 按锚点排序，命中项按 `score desc + id asc` 排序。
- `traceable-source`：每条机器规则必须携带 `src` 绝对路径。
- `lint-or-remove`：无法稳定静态 lint 的条款不继续保留在宪法库中。

## 6. 内联导航索引
- 技能说明：`SKILL.md`
- 宪法基线入口：`assets/goal/MOL_FULL_CANON.md`
- 查询工具入口：`scripts/constitution_keyword_query.py`
- 静态 lint 入口：`scripts/run_constitution_lints.py`
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
│   ├── run_constitution_lints.py
│   ├── build_machine_anchor_docs.py
│   └── constitution_lint_rules/
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
- lint 工具仅承载静态 gate；运行态 gate 不在本技能内实现。
