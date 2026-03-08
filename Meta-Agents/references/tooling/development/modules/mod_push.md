# mod_push

- 入口：`scripts/managed_push.py`
- 职责：把技能内托管副本回写到 registry 中记录过的 `source_path`。
- 不变量：
  - 只允许写回已登记目标。
  - 不允许通过扫描推断目标。
  - `--all` 和指定路径都以 registry 为准。
