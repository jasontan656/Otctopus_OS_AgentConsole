# Cli_Toolbox 开发文档（入口）

适用技能：`Constitution-knowledge-base`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具入口
1. `Cli_Toolbox.constitution_keyword_query` -> `scripts/constitution_keyword_query.py`
2. `Cli_Toolbox.run_constitution_lints` -> `scripts/run_constitution_lints.py`

## 单一职责
- `constitution_keyword_query`：双语关键词查询与机械 JSONL 输出。
- `run_constitution_lints`：对目标仓库执行静态 lint gate。
- 两者都只对可静态验证合同负责，不承载运行态证据检查。

## 输入合同
- `constitution_keyword_query`
  - `--keywords-zh`：中文关键词（必填）。
  - `--keywords-en`：英文关键词（必填）。
  - 禁止参数：`--out/--output/--file/--save/--export/--write/--dump/--path`。
- `run_constitution_lints`
  - `--target`：目标仓库根目录（必填）。

## 输出合同
- `constitution_keyword_query`
  - `query_meta`
  - `minimum_keyword_contract`
  - `constitution_rule`
  - `no_hit`
  - `constitution_enforcement_contract`
- `run_constitution_lints`
  - 单个 JSON 对象：`target/gates/summary`
  - 任一 gate 失败时返回非零退出码。
- 禁止任何 markdown 正文输出。

## 关联策略
1. 查询工具读取 `ANCHOR_DOC_REGISTRY.yaml`、`MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`、`anchor_docs_machine_v1.jsonl`。
2. lint 工具只实现保留下来的静态 gate：
   - `code_governance_gate`
   - `fat_file_gate`
   - `file_structure_gate`
   - `folder_structure_gate`
   - `modularity_gate`
   - `typed_contract_gate`
   - `payload_normalize_gate`
   - `permission_boundary_gate`
   - `hardcoded_asset_gate`
   - `absolute_path_gate`
3. 无法稳定静态验证的条款不再进入 registry 与 gate。

## 示例命令（强制：一行可复制）
- `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Constitution-knowledge-base && python3 scripts/constitution_keyword_query.py --keywords-zh "队列,门禁" --keywords-en "queue,gate" | cat`
- `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Constitution-knowledge-base && python3 scripts/run_constitution_lints.py --target /home/jasontan656/AI_Projects/Octopus_CodeBase_Backend | cat`

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
- 2026-03-06：新增 `Cli_Toolbox.run_constitution_lints`，补齐保留条款的 lint 执行入口。
