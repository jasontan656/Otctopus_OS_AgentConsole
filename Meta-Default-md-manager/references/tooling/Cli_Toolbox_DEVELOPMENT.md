# Cli_Toolbox Development Notes

- The active CLI is rebuilt from the current runtime contracts and asset governance model.
- Rule assets must remain externalized under `rules/`.
- `scaffold` must create external skeletons, internal managed files, and the matching governed path registration together.
- `scan` must keep filename rules, keyword rules, and disallowed lists outside the executable code.
- `scan`, `collect`, and `push` must all expose `--dry-run`.
- `scaffold` must expose `--dry-run`.
- `scan`, `lint`, `collect`, and `push` should support both substring filtering and exact `--source-path` filtering.
- `collect` must update mirror assets and installed skill assets together.
- `collect` must treat external managed files as the truth source.
- `push` must export managed templates outward with `--dry-run` support before any write.
- `push` must treat internal managed templates as the truth source.
