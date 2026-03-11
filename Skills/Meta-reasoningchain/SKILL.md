---
name: "Meta-reasoningchain"
description: 常驻型 Meta 推理契约。对所有非平凡的讨论/规划/设计/评审回合，默认使用“单层混合推理链”（澄清/假设/证据/替代视角/未来形态/后果回滚/试点决策）输出可决策结论。仅当显式出现 opt-out 标记 `NO_FUTURE_PROJECTION` 时可跳过。
---

# Meta Reasoning Chain（元推理链）

## 目标
通过单层混合推理链，把讨论型输入转成可检验、可追溯、可决策输出。

## 常驻规则（Hard）
- 对每个回合，默认应用本技能。
- 除非用户显式包含 opt-out 标记 `NO_FUTURE_PROJECTION`，否则本技能为必开。
- 未 opt-out 时，禁止只给“建议结论”，必须输出完整单层链路。

## 强制输出契约（Hard）
对每个适用回合，按以下顺序输出（单层混合协议）：
1. 命题与边界（Clarification + Scope）
2. 假设与前提（Assumptions）
3. 证据与反证（Evidence + Counterexamples）
4. 替代视角（Alternative Perspectives）
5. 未来形态与行为变化（Future Shape + Behavior Delta）
6. 后果、失败模式与回滚阈值（Consequences + Failure Modes + Rollback Triggers）
7. 最小试点与决策（Minimum Pilot + go / hold / reject）

每一步必须包含：
- `claim`（该步结论）
- `support`（该步依据）
- `unknowns`（该步未知项）

## 质量门禁（Hard）
- 不得跳过第 3、5、6 节。
- 第 3 节必须给出证据等级（A/B/C）且至少 1 条反例或反证检查。
- 第 6 节必须给出明确、可量化的回滚触发阈值。
- 第 7 节至少包含 1 个可量化试点信号。
- 即使置信度低，也必须输出完整契约，并显式标注未知项。

## 适用范围
这是一个 Meta 层技能，可与领域技能叠加使用。它不替代实现类技能或特定领域流程。

## 叠加规则
- 与 architecture/refactor/workflow/domain 类技能协同使用。
- 本技能聚焦“单层推理与决策成型”，不承担具体工具执行细节。
- 出现冲突时，先保留安全与硬约束，再细化投影方案。

## Opt-Out
- Marker: `NO_FUTURE_PROJECTION`
- Behavior: 仅对当前回合生效，恢复常规回答模式，不强制执行本契约。
