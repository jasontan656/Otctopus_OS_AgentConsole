# mod_sync

- 入口：`scripts/managed_sync.py`
- 职责：把技能内托管副本回写到 registry 中记录过的 `source_path`。
- 不变量：
  - 只允许写回已登记目标。
  - `--all` 和指定目标都以 registry 为准。
