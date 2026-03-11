# 通用锚点：typed_contract（类型契约静态合同）

anchor_id: `common_typed_contract`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 固化输入、输出、事件、存储的结构边界，防止字段漂移。
- 为跨模块协作和跨版本兼容提供稳定协议。
- 把契约破坏前移到静态检查阶段。

## 适用范围（必须全覆盖）

| 契约类型 | 适用对象 |
|---|---|
| `request_contract` | API、webhook、管理入口输入 |
| `response_contract` | API、worker、adapter 输出 |
| `event_contract` | 队列与事件 payload |
| `storage_contract` | 数据模型与迁移字段 |
| `config_contract` | 运行配置与策略参数 |

## 写法风格（命令式）
- 先写字段清单，再写验证模式，再写兼容声明。
- 必填和可选字段必须分开定义。
- 契约变更必须显式标注版本变化。

## 类型契约合同（Project Required）

| 字段 | 类型 | 规则 |
|---|---|---|
| `contract_name` | string | 必填，稳定唯一名 |
| `contract_version` | string | 必填，语义化版本 |
| `required_fields` | array | 必填字段集合 |
| `optional_fields` | array | 可选字段集合 |
| `validation_mode` | string | `strict/compat` |
| `compatibility` | string | `backward/forward/bidirectional` |

## 扩展合同（按需）
- `schema_ref`: 外部 schema 文件引用路径。
- `migration_ref`: 存储契约变更迁移脚本引用。
- `test_ref`: 契约验证测试引用。

## 必须做（Do）
1. 先定义契约，再实现业务逻辑。
2. 契约升级必须同步更新 `contract_version` 与兼容说明。
3. 契约文件必须保留 `required_fields/optional_fields` 的显式边界。
4. 契约变更必须附迁移引用或兼容声明。
5. 发布前执行类型契约静态检查，失败阻断。

## 不要做（Don't）
1. 不要在核心链路传递无约束对象。
2. 不要无版本直接改字段语义。
3. 不要只改文档不改契约定义。
4. 不要省略契约名称与验证模式。

## 为什么（Why）
1. 类型契约是并发协作的最低共识层。
2. 版本化和兼容策略可降低灰度冲突概率。
3. 静态校验能把错误拦截在实现前期。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "common_typed_contract" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common

# 2) 契约字段存在性检查
rg -n "contract_name|contract_version|required_fields|optional_fields|validation_mode" src backend runtime -S
```

## 最小验收
1. 核心契约文件都声明 `contract_name/contract_version`。
2. 契约文件都显式区分 `required_fields` 与 `optional_fields`。
3. 契约静态检查失败时会阻断 CI。
