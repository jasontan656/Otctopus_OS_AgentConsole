# AGENTS Branch Index

- 当前分支只治理一个外部目标：`Octopus_OS/AGENTS.md`。
- 机器主索引：`assets/mother_doc_agents/registry.json`。
- 人类审计索引：`assets/mother_doc_agents/index.md`。
- 受管内部资产：
- `assets/managed_targets/Octopus_OS/AGENTS_human.md`
- `assets/managed_targets/Octopus_OS/AGENTS_machine.json`

## Stage Order

1. `scan`: 发现根目标与所有非法额外 `AGENTS.md`。
2. `collect`: 将外部根 `AGENTS.md` 收回为 managed human/machine pair。
3. `push`: 将 managed pair 写回根 `AGENTS.md`，并删除其他非法 `AGENTS.md`。
