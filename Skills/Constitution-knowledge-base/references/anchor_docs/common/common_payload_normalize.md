# 通用锚点：payload_normalize（载荷归一化静态合同）

anchor_id: `common_payload_normalize`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `backend_domain`

## 在项目中起什么作用
- 将 Telegram、Codex、Web、Admin、API 输入统一到稳定协议。
- 避免下游模块直接依赖渠道特定字段，降低耦合。
- 保证归一化入口唯一且可静态定位。

## 适用范围（必须全覆盖）

| 输入来源 | 归一化目标 |
|---|---|
| `telegram` | update/callback/webapp_data 统一映射 |
| `codex` | exec 事件统一映射 |
| `http_api` | query/body/header 合并映射 |
| `internal_queue` | 任务 payload 统一契约映射 |

## 归一化合同（Project Required）

| 字段 | 类型 | 规则 |
|---|---|---|
| `trace_id` | string | 必填 |
| `session_id` | string | 必填 |
| `actor_id` | string | 必填 |
| `channel` | string | `telegram/codex/web/admin/api/queue` |
| `payload_version` | string | 必填，语义化版本 |
| `schema_name` | string | 归一化契约名 |
| `raw_ref` | string | 原始载荷引用键 |

## 必须做（Do）
1. 所有入口在业务逻辑前必须完成归一化。
2. 归一化模块必须保留 `payload_version/schema_name/raw_ref`。
3. 下游模块只能读取统一字段，不得读取渠道私有字段。
4. 发布前执行归一化静态检查，失败阻断。

## 不要做（Don't）
1. 不要在多个模块重复实现归一化逻辑。
2. 不要无版本号变更归一化结构。
3. 不要让下游直接解析原始渠道 payload。
4. 不要丢失 `raw_ref` 关联。

## 为什么（Why）
1. 统一输入模型是跨渠道稳定运行的前提。
2. 单点归一化可显著降低维护和排障成本。
3. 静态约束可以防止私有字段向下游扩散。

## 实操命令（项目级）

```bash
rg -n "common_payload_normalize" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common
python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Dev-PythonCode-Constitution-Backend/scripts/run_python_code_lints.py --target . | jq '.gates[] | select(.gate=="payload_normalize_gate")'
```

## 最小验收
1. 核心入口归一化文件都声明 `payload_version/schema_name/raw_ref`。
2. 下游模块不直接读取渠道私有字段。
3. 归一化静态检查失败时会阻断 CI。
