---
name: prompt_workflow_mode
description: 提示/规则工作流模式。面向 prompts、workflows、rules、constitutions 等主要通过自然语言影响模型决策轨迹的对象，要求通过触发矩阵、轨迹 oracle 和写回语义来证明行为保持。
---

# 提示/规则工作流模式

## 1. 模式目标
- 适用于 prompts、workflow、rules、constitutions 以及任何通过自然语言驱动模型决策的工件。
- 在改写结构、压缩体积、调整布局或升级表达时，保持工作流语义和受保护可观察合同不退化。

## 2. 模式核心定义
- 行为不只看最终输出，还包括：
  - 触发/路由决策
  - 工具调用轨迹
  - 写回语义
  - 诊断/审计可观察信号
- 等价判断依据是 witness set 下的可观察效果，而不是文本相似度。

## 3. OEC（可观察效果合同）
```yaml
oec:
  mode: "strict_refactor | contract_preserving_upgrade"
  artifact: "<被重构对象>"
  consumer: ["<reader|workflow|downstream_model|audit>"]
  stimuli:
    - "<输入场景>"
  observables:
    - "<必须保持的外部现象>"
  invariants:
    - "<绝对不能变>"
  allowed_deltas:
    - "<允许变化>"
  witness_set:
    - id: "W1"
      stimulus: "<代表性输入>"
      oracle: "<轨迹或输出检查>"
  protected_observability_contracts:
    - "<诊断/日志/事件/输出通道>"
  quality_gain_targets:
    - "<至少一个显式质量增益>"
```

额外必须补充：
- `instruction_priority_model`
- `tooling_surface_contract`
- `routing_contract`
- `trace_observables`
- `write_semantics`

## 4. 硬门槛
- 必须先定义 OEC。
- 必须先产出 `workflow_model_v1`。
- 必须先产出 `trigger_contract_matrix_v1`。
- witness set 必须从 matrix 派生。
- 每个 witness case 都必须有 trajectory-aware oracle。
- 必须先 baseline，再改写，再重跑 witness set。

禁止项：
- 禁止把 prompt 改写退化成“无限边缘 case 枚举补丁”。
- 禁止没有 matrix、没有 oracle 就宣称行为保持。

## 5. 执行协议

### 5.1 Workflow Model v1
```yaml
workflow_model_v1:
  states:
    - id: "<state_id>"
      purpose: "<一句话目标>"
      entry_triggers:
        - "<触发条件>"
      required_observables:
        - "<必须出现的 marker/log/event/output>"
  routing_rules:
    - when: "<条件>"
      must_route_to: "<state_id>"
      must_not_route_to: ["<state_id>"]
  tool_surface:
    allowed_tools: ["<tool>"]
    forbidden_actions:
      - "<禁止动作>"
  write_semantics:
    - "<artifact>": "<merge/overwrite/idempotency 规则>"
```

### 5.2 Trigger / Contract Matrix v1
```yaml
trigger_contract_matrix_v1:
  - id: TM-01
    stimulus: "<输入场景>"
    expected_routing: "<应进入的状态或分支>"
    tool_trajectory_invariants:
      must_call: ["<tool>(<key params>)"]
      must_not_call: ["<tool>"]
    protected_observables:
      - "<marker/log/event/output>"
    oracle: "<trajectory diff / marker presence / output assertions>"
    allowed_delta: "<若有>"
```

规则：
- 第一轮最多 20 条；超出时必须抽象聚类。
- 每个分支至少一个 witness。
- 不能只覆盖 happy path。

### 5.3 Witness Set 覆盖面
至少覆盖：
- 每个 routing branch
- 写回与幂等场景
- partial-write recovery
- failure / recovery

## 6. 等价方法

### 6.1 叙事型工件
适用：docs / article / long-form guidance

要求：
- 不新增原本没有的核心语义
- 不丢失原有关键主张
- 不扭曲原定义与约束

可用 oracle：
- reader question list
- claim inventory
- definition inventory

### 6.2 约束型工件
适用：prompt / workflow / constitution / rule set

要求：
- trigger 等价
- application 等价
- authority coherence
- 不制造 legacy parallelism

可用 oracle：
- trigger matrix
- output contract checks
- applied constraint set

## 7. Stop Condition
满足以下条件才可停止：
- matrix 覆盖所有分支与受保护写回/可观察合同
- 每个 witness case 都有 runnable oracle
- baseline 已完成

## 8. 输出契约
完成后必须用中文报告：
- OEC 摘要
- `workflow_model_v1`
- `trigger_contract_matrix_v1`
- witness set 与 oracle
- baseline 方法
- 等价验证结果（PASS/FAIL）
- 至少一个可量化质量增益
