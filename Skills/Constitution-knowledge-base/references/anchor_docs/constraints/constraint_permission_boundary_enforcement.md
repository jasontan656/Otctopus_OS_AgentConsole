# 限制项：permission_boundary_enforcement（权限边界静态强制执行）

anchor_id: `constraint_permission_boundary_enforcement`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制高风险动作经过统一鉴权与作用域定义。
- 防止业务侧临时放行造成越权执行。
- 将权限决策收敛为可静态 gate 的字段与入口检查。

## 权限执行合同（Project Required）

| 字段 | 规则 |
|---|---|
| `actor_type` | 必填，`human/agent/system` |
| `actor_id` | 必填，主体标识 |
| `role` | 必填，稳定枚举 |
| `scope` | 必填，作用域表达式 |
| `action` | 必填，动作枚举 |
| `policy_version` | 必填，策略版本 |
| `authz_result` | `allow/deny/blocked` |
| `deny_code` | `deny/blocked` 时必填 |
| `approval_ref` | 高风险动作必填 |

## 必须做（Do）
1. 执行前必须校验 `actor/role/scope/action` 定义存在。
2. 写操作默认拒绝未声明权限。
3. 拒绝和阻断必须保留 `deny_code`。
4. 高风险动作必须有 `approval_ref`。
5. 静态扫描必须定位绕过统一策略入口的文件。

## 不要做（Don't）
1. 不要在 handler 内部硬编码放行。
2. 不要把知道链接当权限控制。
3. 不要把拒绝结果降级为 warning。
4. 不要允许无 `actor_id` 的高风险动作定义。

## 实操命令（项目级）

```bash
rg -n "constraint_permission_boundary_enforcement" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints
./.venv_backend_skills/bin/python Skills/Dev-PythonCode-Constitution-Backend/scripts/run_python_code_lints.py --target . | jq '.gates[] | select(.gate=="permission_boundary_gate")'
```

## 最小验收
1. 高风险动作审批引用覆盖率达到 100%。
2. `deny/blocked` 定义 `deny_code` 缺失率为 0。
3. 未授权高风险动作定义全部被静态 gate 阻断。
