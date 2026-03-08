# Scan Rules

- 只允许写 scan_report.json。
- 运行前必须拿到技能内 .cli.lock；抢不到锁就显式报错。
- 禁止写 registry.json、index.md 和托管副本。
- 必须扫描默认文档集合：AGENTS.md、.gitignore、Octopus_CodeBase_Backend/README.md、Octopus_CodeBase_Backend/Deployment_Guide.md。
- 必须忽略 Human_Work_Zone/、Codex_Skills_Result/、Codex_Skill_Runtime/、.git/、__pycache__/、.pytest_cache/、虚拟环境与 node_modules/。
- 必须忽略技能自身 assets/managed_targets/。
- 禁止默认跨阶段读取 collect 或 push 指引；除非用户显式要求。
