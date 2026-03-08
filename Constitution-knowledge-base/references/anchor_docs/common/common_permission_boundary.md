# 通用锚点：permission_boundary（权限边界静态合同）

anchor_id: `common_permission_boundary`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 统一谁在什么条件下可以执行什么动作的静态定义。
- 将授权判断从业务散落判断收敛到统一策略入口。
- 为高风险动作提供可扫描的审批与拒绝字段。

## 权限决策合同（Project Required）

| 字段 | 类型 | 规则 |
|---|---|---|
| `actor_id` | string | 必填，可追溯到主体 |
| `actor_type` | string | `human/agent/system` |
| `role` | string | 必填，稳定枚举 |
| `scope` | string | 必填，资源作用域表达式 |
| `action` | string | 必填，动作枚举 |
| `policy_version` | string | 必填，策略版本 |
| `authz_result` | string | `allow/deny/blocked` |
| `deny_code` | string | `deny/blocked` 时必填 |
| `approval_ref` | string | 高风险写动作必填 |

## 必须做（Do）
1. 所有高风险动作必须经过统一授权定义。
2. 默认拒绝未声明策略的动作和资源。
3. `deny/blocked` 结果必须保留 `deny_code`。
4. 高风险动作必须校验 `approval_ref`。
5. 发布前执行权限边界静态检查，失败阻断。

## 不要做（Don't）
1. 不要在业务代码中散落硬编码放行逻辑。
2. 不要把前端隐藏按钮当作权限控制。
3. 不要允许无 `actor_id` 的高风险动作定义。
4. 不要绕过统一策略入口直接调用执行器。

## 为什么（Why）
1. 统一授权链路可以把越权风险收敛到单点治理。
2. 策略版本化能让权限变更具备可追溯性。
3. 拒绝结果结构化后，能快速定位策略缺口与误配。

## 实操命令（项目级）

```bash
rg -n "common_permission_boundary" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common
python3 scripts/run_constitution_lints.py --target . | jq '.gates[] | select(.gate=="permission_boundary_gate")'
```

## 最小验收
1. 高风险写动作 `approval_ref` 覆盖率为 100%。
2. 拒绝定义 `deny_code` 缺失率为 0。
3. 权限静态检查失败时会阻断 CI。
