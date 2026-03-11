# 限制项：payload_normalization_enforcement（载荷归一化静态强制执行）

anchor_id: `constraint_payload_normalization_enforcement`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制所有入口在业务处理前定义统一归一化结构。
- 防止渠道字段差异扩散到下游业务模块。
- 将归一化约束收敛为可静态 gate 的字段与边界检查。

## 归一化执行合同（Project Required）

| 字段 | 规则 |
|---|---|
| `trace_id` | 必填 |
| `session_id` | 必填 |
| `actor_id` | 必填 |
| `channel` | 必填，渠道枚举 |
| `payload_version` | 必填，语义化版本 |
| `schema_name` | 必填 |
| `raw_ref` | 必填，原始载荷引用 |

## 必须做（Do）
1. 所有入口必须执行归一化定义。
2. 下游业务层禁止直接读取原始渠道字段。
3. 归一化静态检查必须输出泄漏文件路径与缺失字段。
4. 归一化版本变更必须同步更新契约文件。

## 不要做（Don't）
1. 不要在业务层重复实现归一化。
2. 不要让下游直接读取渠道原始字段。
3. 不要丢失 `raw_ref`。
4. 不要绕过统一 schema 命名。

## 实操命令（项目级）

```bash
rg -n "constraint_payload_normalization_enforcement" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints
python3 scripts/run_constitution_lints.py --target . | jq '.gates[] | select(.gate=="payload_normalize_gate")'
```

## 最小验收
1. 关键入口归一化定义完整率为 100%。
2. 原始字段泄漏场景全部被静态 gate 阻断。
