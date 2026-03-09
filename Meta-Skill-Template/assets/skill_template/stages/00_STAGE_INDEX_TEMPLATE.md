# Stage Index Template

## 抽象层
- [列出 top-level always-load 规则与 resident docs。]
- [列出统一 CLI 入口。]

## 阶段集合
| stage_id | objective | entry_contracts | exit_signal |
|---|---|---|---|
| `replace_me` | `replace_me` | `replace_me` | `replace_me` |

## resident docs
- `replace_me`

## 切换规则
- 当前阶段完成后，显式丢弃上一阶段 checklist、focus、模板填写上下文。
- 下一阶段开始前，重新读取该阶段 CLI 合同。
- 阶段域必须独立成块书写，不得混写。
