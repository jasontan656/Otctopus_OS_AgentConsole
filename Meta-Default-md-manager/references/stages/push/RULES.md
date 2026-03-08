# Push Rules

- 只允许基于 `registry.json` 里的目标回写。
- 运行前必须拿到技能内 `.cli.lock`，抢不到锁就显式报错。
- `registry.json` 不存在、为空或无条目时，必须显式报错。
- 禁止通过扫描推断目标。
- 禁止写技能目录外的新路径。
- `--all` 和指定路径都必须受 registry 约束。
