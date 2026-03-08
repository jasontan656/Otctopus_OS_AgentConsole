# 限制项：typed_contract_enforcement（类型契约静态强制执行）

anchor_id: `constraint_typed_contract_enforcement`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制关键输入输出采用显式类型契约。
- 防止字段漂移和隐式协议破坏进入代码库。
- 把类型破坏前移到静态 gate 阶段阻断。

## 契约执行合同（Project Required）

| 字段 | 规则 |
|---|---|
| `contract_name` | 必填，稳定唯一 |
| `contract_version` | 必填，语义化版本 |
| `required_fields` | 必填字段集合 |
| `optional_fields` | 可选字段集合 |
| `validation_mode` | `strict/compat` |
| `compatibility` | 兼容策略声明 |

## 必须做（Do）
1. 所有入口/出口契约都版本化。
2. 契约变更必须记录兼容策略与迁移路径。
3. 静态扫描必须覆盖契约核心字段并阻断缺失。
4. 契约 lint 报告必须给出缺失文件与缺失字段。

## 不要做（Don't）
1. 不要接收未定义字段集合。
2. 不要无版本变更字段语义。
3. 不要绕过契约文件直接扩展 payload。
4. 不要只改注释不改契约主体。

## 实操命令（项目级）

```bash
rg -n "constraint_typed_contract_enforcement" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints
python3 scripts/run_constitution_lints.py --target . | jq '.gates[] | select(.gate=="typed_contract_gate")'
```

## 最小验收
1. 核心链路契约文件字段完整率为 100%。
2. 契约缺失场景全部被静态 gate 阻断。
