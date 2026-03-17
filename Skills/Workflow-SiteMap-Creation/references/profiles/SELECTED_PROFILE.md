# Selected Profile

- doc_topology: `workflow_path`
- tooling_surface: `automation_cli`
- workflow_control: `compiled`

## Why This Profile

- `workflow_path`：本技能必须承载稳定入口与明确步骤链，而不是把完整治理链塞回门面。
- `automation_cli`：本技能需要实际执行 factory 化转换、`INTENT:` 强化、tmux subagent 启动与轮询、runtask 证据汇总、产物刷新、lint 审计与 mirror 同步。
- `compiled`：本技能是固定上游协作技能，不允许退化成泛化 brainstorming，也不允许把九阶段闭环折叠回单段叙事。

## Governance Consequence

- 任何新增规则都必须同步反映到：
  - `path/`
  - `references/governance/`
  - `references/runtime_contracts/`
  - `scripts/`
- 任何 workflow 变动都必须继续满足 `references/runstates/` 的中间态消费与写回要求。
- 任何主链变动都必须继续保持：
  - `factory -> Meta-Enhance-Prompt -> tmux subagent -> Functional-Analysis-Runtask -> artifact refresh -> validation closeout`
