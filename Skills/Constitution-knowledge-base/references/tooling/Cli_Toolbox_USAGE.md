# Cli_Toolbox 使用文档

适用技能：`Constitution-knowledge-base`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- `Cli_Toolbox.constitution_keyword_query` -> `scripts/constitution_keyword_query.py`

## 叙事式使用说明（固定格式）

### Cli_Toolbox.constitution_keyword_query
- 人类叙事版输入：
  - 我想用中英关键词快速检索宪法，且输出必须是给 AI 消费的紧凑机械 JSONL，不要人类正文噪音。
- 电脑动作发生了什么：
  - 脚本读取 `ANCHOR_DOC_REGISTRY.yaml` 与 `MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`。
  - 脚本读取 `references/anchor_docs_machine/anchor_docs_machine_v1.jsonl` 作为唯一查询语料。
  - 接收 `--keywords-zh` 与 `--keywords-en`（双语必填），计算域关联命中。
  - 始终打印完整 `common_core` 机器规则；然后只打印真实命中的 `common_conditional/constraints` 机器规则（含绝对路径）。
  - 强制输出 `JSONL`，禁止 markdown 正文输出。
  - 禁止落盘参数；若传 `--out/--output/--file/--save/...` 直接报错。
- 人类叙事版输出：
  - 控制台输出多行 JSON，每行一个机械规则对象，可直接给模型消费，不需要再做正文清洗。

## 示例命令（强制：一行可复制）
- 最小用途描述：双语关键词检索机器版宪法 JSONL（始终带 common_core，全程仅控制台输出）。
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Constitution-knowledge-base && python3 scripts/constitution_keyword_query.py --keywords-zh "会话,队列" --keywords-en "session,queue" | cat`
- 禁止事项（强制）：
  - 查询命令禁止限制输出行数；禁止使用 `sed -n/head/tail/awk 'NR...'` 等限行命令。

## 参数与结果（供 AI/工程使用）
- `constitution_keyword_query` 输入：
  - `--keywords-zh`（必填）
  - `--keywords-en`（必填）
- 共同输出：
  - 仅控制台输出。
- 查询输出：
  - `query_meta`
  - `minimum_keyword_contract`
  - `constitution_rule`
  - `no_hit`
  - `constitution_enforcement_contract`
- 失败码约定：
  - `2`：参数错误。
  - `1`：运行期异常。

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
