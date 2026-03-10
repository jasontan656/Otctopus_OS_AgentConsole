---
name: runnable_artifacts_mode
description: 可执行工件模式。面向 code、tool、runner、script 等主要通过机器执行体现行为的对象，要求在重构或迁移前先把当前行为反编译为可检查的行为合同，再用 witness set 与可执行 oracle 验证等价。
---

# 可执行工件模式

## 1. 模式目标
- 适用于代码、工具、脚本、runner、executor、orchestrator 等可执行工件。
- 在改变内部结构时，保持工作流语义、输出合同和受保护可观察性不退化。

## 2. 模式核心定义
- 行为 = 特定消费者可观察到的外部效果。
- 等价 = Observable-Effect Equivalence（OEC，可观察效果等价）。
- 重构必须至少带来一个可度量的质量增益；否则只是 churn。

## 3. OEC（可观察效果合同）
若无法写出 OEC，就还不能开始重构。

```yaml
oec:
  mode: "strict_refactor | contract_preserving_upgrade"
  artifact: "<被重构对象>"
  consumer: ["<reader|workflow|downstream_model|audit>"]
  stimuli:
    - "<如何触发>"
  observables:
    - "<哪些外部现象必须保持>"
  invariants:
    - "<绝对不能变>"
  allowed_deltas:
    - "<允许变化>"
  witness_set:
    - id: "W1"
      stimulus: "<代表性输入>"
      oracle: "<如何检查等价>"
  protected_observability_contracts:
    - "<不能消失或改变语义的诊断/日志/事件/输出通道>"
  quality_gain_targets:
    - "<至少一个显式质量增益>"
```

模式约束：
- `strict_refactor`：除非显式写进 `allowed_deltas`，否则不允许任何外部可观察变化。
- `contract_preserving_upgrade`：允许展示、性能、体验类提升，但工作流语义与受保护可观察合同不得退化。

## 4. 硬门槛
- 必须先定义 OEC。
- 必须先产出 `system_model_v1`。
- 必须先产出 `contract_matrix_v1`。
- witness set 必须从 `contract_matrix_v1` 派生，不能自由散列。
- 每个 witness case 都必须有可执行 oracle。
- 必须在改动前完成 baseline，改动后重新验证。

禁止项：
- 禁止只靠“看起来差不多”宣称等价。
- 禁止大而散的 case 清单，没有 matrix、没有 oracle、没有收敛边界。

## 5. 执行协议

### 5.1 代码反编译为行为合同
当没有 requirements doc 时，当前代码行为就是唯一权威。

从所有入口点回溯：
- CLI 命令、flag、env、config
- public API
- route / handler / consumer
- timer / worker / watcher
- UI/TUI 事件入口

每个入口都写成：
`Trigger -> State Change -> Output Change -> Side Effects`

行为陈述模板：

```yaml
behavior_statements:
  - id: "B-01"
    strength: "Hard | Soft | Undefined"
    trigger: "<事件 + 前置条件>"
    state_change: "<必须变化的状态>"
    output_change: "<输出变化>"
    side_effects: "<IO/network/cache/log/metrics>"
```

### 5.2 System Model v1
```yaml
system_model_v1:
  modules:
    - name: "<module>"
      responsibility: "<一句话职责>"
  state:
    - name: "<state>"
      owner: "<module>"
      lifecycle: "<创建/更新/清理>"
  event_flow:
    - stimulus: "<输入>"
      path: "<entrypoint -> handlers -> effects>"
  io_contracts:
    reads:
      - "<读取对象>"
    writes:
      - "<写入对象 + merge/overwrite 语义>"
  failure_modes:
    - "<失败类型> -> <外部表现>"
```

### 5.3 Contract Matrix v1
```yaml
contract_matrix_v1:
  - id: CM-01
    contract: "<一条外部可观察规则>"
    stimulus: "<触发方式>"
    observables:
      - "<必须为真的外部现象>"
    oracle: "<diff/snapshot/assertion/trace invariant>"
    allowed_delta: "<若有>"
    risk_if_broken: "<破坏风险>"
```

规则：
- 第一轮最多 20 条；超出时必须抽象聚类。
- witness set 必须来自 matrix。

## 6. 基线与 Oracle
- 必须先 baseline，再重构。
- 可用 oracle：
  - golden master
  - snapshot assertions
  - trace invariants
  - property / invariant tests

若输出有 nondeterminism：
- 必须先定义 normalize 规则，再做 baseline。

## 7. 等价检查
除非写进 `allowed_deltas`，否则必须保持：
- 主输出
- 成功/失败分类与 exit code
- 顺序 / phase 语义
- 受保护可观察合同

## 8. 输出契约
完成后必须用中文报告：
- OEC 摘要
- `system_model_v1`
- `contract_matrix_v1`
- `behavior_statements` 摘要
- witness set 与 oracle
- baseline 方法
- 等价验证结果（PASS/FAIL）
- 至少一个可量化质量增益
