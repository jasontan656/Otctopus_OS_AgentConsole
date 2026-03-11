# Cli_Toolbox 开发文档（入口）

适用技能：`Constitution-knowledge-base`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具入口
1. `Cli_Toolbox.constitution_keyword_query` -> `scripts/constitution_keyword_query.py`

## 单一职责
- `constitution_keyword_query`：双语关键词查询与机械 JSONL 输出。
- 宪法库当前不再内置 lint CLI；Python 代码 lint 已迁移到 `Dev-PythonCode-Constitution-Backend`。
- 查询工具只对可检索锚点合同负责，不承载运行态证据检查。

## 输入合同
- `constitution_keyword_query`
  - `--keywords-zh`：中文关键词（必填）。
  - `--keywords-en`：英文关键词（必填）。
  - 禁止参数：`--out/--output/--file/--save/--export/--write/--dump/--path`。

## 输出合同
- `constitution_keyword_query`
  - `query_meta`
  - `minimum_keyword_contract`
  - `constitution_rule`
  - `no_hit`
  - `constitution_enforcement_contract`
- 禁止任何 markdown 正文输出。

## 关联策略
1. 查询工具读取 `ANCHOR_DOC_REGISTRY.yaml`、`MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`、`anchor_docs_machine_v1.jsonl`。
2. `common_fat_file` 与 Python lint 已迁移出宪法库，不再作为 `common_core` 查询底座。
3. 无法稳定静态验证的条款不再进入宪法库 registry。

## 示例命令（强制：一行可复制）
- `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Constitution-knowledge-base && python3 scripts/constitution_keyword_query.py --keywords-zh "队列,门禁" --keywords-en "queue,gate" | cat`

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `SKILL.md`
  - `ANCHOR_DOC_REGISTRY.yaml`
  - `anchor_docs_machine_v1.jsonl`（通过构建脚本重建）

## 版本变更记录
- 2026-03-01：新增 `Cli_Toolbox.constitution_keyword_query`，支持双语关键词查询、common_core 全量输出、禁止落盘参数。
- 2026-03-01：查询输出升级为仅机器 JSONL，并引入 `anchor_docs_machine_v1.jsonl`。
- 2026-03-06：移除不可静态验证的运行态条款，仅保留静态 gate 合同。
- 2026-03-12：迁出 Python lint 与胖文件治理，宪法库回到 query-only 边界。
