# Cli_Toolbox Development Notes

- The active CLI is rebuilt from the current runtime contracts and asset governance model.
- Rule assets must remain externalized under `rules/`.
- `scaffold` must consume the `骨架生成模版`, create external skeletons, create the first internal `治理映射模版` files, and register the matching governed path together.
- `scan` must keep filename rules, keyword rules, and disallowed lists outside the executable code.
- `scan`, `collect`, and `push` must all expose `--dry-run`.
- `scaffold` must expose `--dry-run`.
- `scan`, `lint`, `collect`, and `push` should support both substring filtering and exact `--source-path` filtering.
- `collect` must update mirror assets and installed skill assets together.
- `collect` must treat external managed files as the truth source.
- `push` must export the `治理映射模版` outward with `--dry-run` support before any write.
- `push` must treat the internal `治理映射模版` as the truth source.
