# Stage Index Template

## 顶层常驻文档
- `replace_me`

## 统一入口
- `python3 scripts/Cli_Toolbox.py stage-checklist --stage <stage> --json`
- `python3 scripts/Cli_Toolbox.py stage-doc-contract --stage <stage> --json`
- `python3 scripts/Cli_Toolbox.py stage-command-contract --stage <stage> --json`
- `python3 scripts/Cli_Toolbox.py stage-graph-contract --stage <stage> --json`

## 阶段集合
| stage_id | objective | checklist | doc_contract | command_contract | graph_contract | exit_signal |
|---|---|---|---|---|---|---|
| `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` |

## resident docs 规则
- 跨阶段只保留顶层常驻文档。
- resident docs 负责维持全局边界，不负责承载某阶段细节。

## 切换规则
- 当前阶段完成后，显式丢弃上一阶段 checklist、stage docs、模板填写上下文与临时 focus。
- 下一阶段开始前，重新读取该阶段四类合同。
