---
owner: "由 `Otctopus_OS_AgentConsole` repository root container 所代表的 公共说明面 负责；当前通过 `$Meta-RootFile-Manager` 的 `README_MD` 通道受管并同步。"
---
# Otctopus_OS_AgentConsole

`Otctopus_OS_AgentConsole` 是 `/home/jasontan656/AI_Projects` 下的 repo-local skill truth source。

它承接的是真源、治理与同步职责，不再承接独立产品门面、安装器或 console 包装叙事。

## What Lives Here

- `Skills/`
  - repo 内技能真源、治理文档、CLI 与测试。
- `SkillsManager-Mirror-To-Codex`
  - 负责把 repo 内真源同步到 `~/.codex/skills`。
- `docs/THIRD_PARTY_COMPONENTS.md`
  - 当前保留的仓库级补充文档，用于说明第三方衍生代码与许可证边界。
- repo root files
  - 由 `Meta-RootFile-Manager` 负责受管维护。

## Working Boundaries

- 技能改动先回到 repo 内 `Skills/` 真源，再按需同步到 `~/.codex/skills`。
- runtime 与 result 根统一从 `/home/jasontan656/AI_Projects` 推导：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result`
- 任务分析产物固定先落到 `/home/jasontan656/AI_Projects/Human_Work_Zone` 受管根。
- `README.md`、`AGENTS.md` 与其他受管 root files 通过 `Meta-RootFile-Manager` 的 internal truth -> centered push -> lint 主链维护。

## Repository Layout

- `Skills/`: all skill roots, including `.system/`
- `docs/`: repository-level support docs
- repository root: governed entry files such as `README.md`, `AGENTS.md`, and repository metadata

## Third-Party Components

This repository includes a third-party-derived code component inside `Skills/Meta-code-graph-base/assets/gitnexus_core`.

- `Meta-code-graph-base` vendors and modifies core code migrated from the `GitNexus` project.
- Its separate upstream license notices remain in the vendored directory.
- See `docs/THIRD_PARTY_COMPONENTS.md` for the current scope, source path, and licensing summary.
