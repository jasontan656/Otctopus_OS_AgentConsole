# Cli_Toolbox Architecture Overview

适用技能：`2-Octupos-FullStack`

## 当前范围

- 一个统一 CLI 入口下，显式分离三阶段合同读取：
  - checklist
  - doc contract
  - command contract
  - graph contract
- `Cli_Toolbox.py` 保持薄入口，只负责 parser 根装配与命令分发。
- `cli_parser_blocks.py` 负责成组注册 parser，避免入口脚本继续膨胀。
- `skill_runtime_entry.py` 负责输出 skill 级 runtime/facade JSON 合同，供模型先读 CLI 再下钻阶段或子分支。

## Mother_Doc Structure

- `Mother_Doc` 每层目录都必须具备：
  - `README.md`
  - `<folder_name>.md`
- `Mother_Doc/docs` 树不再维护递归 `AGENTS.md`。
- `mother_doc` 阶段内部再拆三条链：
  - `direct_writeback`
  - `question_backfill`
  - root-only `AGENTS manager`
- root-only `AGENTS manager` 进一步固定为：
  - `scan`
  - `collect`
  - `push`
- 根外部 `AGENTS.md` 当前只允许 `Octopus_OS/AGENTS.md` 一个目标。
- 文档必须具备 `Document Status + Block Registry`。
- `Mother_Doc/docs/Mother_Doc/common/development_logs/` 由 `evidence` 阶段维护，用于承接 implementation batch 与 deployment checkpoint 时间线。
