---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "Cli_Toolbox operational usage for Meta-Skill-DocStructure"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The toolbox commands operationalize the runtime contract."
  - target: "development/modules/mod_anchor_graph_lint.md"
    relation: "details"
    direction: "downstream"
    reason: "The lint and graph module doc explains implementation behavior."
---

# Cli_Toolbox 使用文档

适用技能：`Meta-Skill-DocStructure`

## 工具清单
- `Cli_Toolbox.runtime_contract`
  - `python3 scripts/Cli_Toolbox.py runtime-contract --json`
- `Cli_Toolbox.lint_doc_anchors`
  - `python3 scripts/Cli_Toolbox.py lint-doc-anchors --target <skill_root> --json`
- `Cli_Toolbox.build_anchor_graph`
  - `python3 scripts/Cli_Toolbox.py build-anchor-graph --target <skill_root> --json`
- `Cli_Toolbox.rebuild_self_graph`
  - `python3 scripts/Cli_Toolbox.py rebuild-self-graph --json`

## 叙事式使用说明

### `Cli_Toolbox.runtime_contract`
- 人类叙事版输入：
  - 先告诉我这个技能当前到底要求哪些文档结构规则、脚本入口和机器资产。
- 电脑动作发生了什么：
  - 读取 `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`，按原样输出 machine-readable 合同。
- 人类叙事版输出：
  - 返回技能范围、思考链、命令、frontmatter 规范、matrix 资产与 self graph 路径。

### `Cli_Toolbox.lint_doc_anchors`
- 人类叙事版输入：
  - 检查这个 skill 目录下的 markdown 文档是否都带有效 anchor，并判断是否出现需要拆分的信号。
- 电脑动作发生了什么：
  - 递归扫描目标 skill root 下所有 `.md` 文档。
  - 解析 frontmatter，校验 `doc_id/doc_type/topic/anchors`。
  - 校验每份文档至少一个 anchor，且 target 指向 skill 内真实 markdown 文档。
  - 读取 `assets/runtime/anchor_query_matrix.json`，对标题与正文做 split-signal 检查。
- 人类叙事版输出：
  - 返回 `status/errors/warnings/graph_summary`；anchor 缺失是 fail，拆分建议是 warning。

### `Cli_Toolbox.build_anchor_graph`
- 人类叙事版输入：
  - 把某个 skill 内部文档的 anchor 关系图构出来，给模型或脚本继续消费。
- 电脑动作发生了什么：
  - 扫描 markdown 文档，抽取 node 与 edge，归一化 target 路径，输出 JSON graph。
- 人类叙事版输出：
  - 返回 `nodes/edges/summary`，可以直接做后续分析。

### `Cli_Toolbox.rebuild_self_graph`
- 人类叙事版输入：
  - 我改了这个技能自己的文档，请把它自己的 graph JSON 重建回资产目录。
- 电脑动作发生了什么：
  - 对当前技能根目录执行 graph build。
  - 若存在 hard lint error，拒绝写回。
  - 若无 hard error，则回写 `assets/runtime/self_anchor_graph.json`。
- 人类叙事版输出：
  - 返回 `written_graph_path` 与最新 `summary`。

## 快速示例
```bash
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && python3 scripts/Cli_Toolbox.py runtime-contract --json | sed -n '1,200p'
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && python3 scripts/Cli_Toolbox.py lint-doc-anchors --target /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure --json | sed -n '1,240p'
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && python3 scripts/Cli_Toolbox.py rebuild-self-graph --json | sed -n '1,240p'
```

## 参数与结果
- 输入：
  - `target: absolute skill root path`
  - `json: bool`
- 输出：
  - `runtime-contract`: `contract_name/contract_version/commands/assets`
  - `lint-doc-anchors`: `status/errors/warnings/summary`
  - `build-anchor-graph`: `nodes/edges/summary`
  - `rebuild-self-graph`: `status/written_graph_path/summary`

## 失败码约定
- `1`: lint 失败或 graph 构建失败
- `2`: 输入目录非法或不是 skill root
- `3`: frontmatter 解析失败
