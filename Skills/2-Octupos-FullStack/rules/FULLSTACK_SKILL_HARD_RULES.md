# FULLSTACK Skill Hard Rules

1. `Octopus_OS/AGENTS.md` 是当前唯一允许存在的外部 AGENTS runtime entry。
2. AGENTS manager 只允许执行 `scan / collect / push`。
3. mirror 内部只保留 `assets/managed_targets/Octopus_OS/AGENTS_human.md` 与 `assets/managed_targets/Octopus_OS/AGENTS_machine.json`。
4. 任何额外 `Octopus_OS/**/AGENTS.md` 都必须被清理。
5. `mother_doc`、`implementation`、`evidence` 三阶段仍然存在，但 AGENTS 治理只占 `mother_doc` 中的一条极小子路径。
