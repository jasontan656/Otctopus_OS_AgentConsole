# Facade Load Map

适用技能：`Disabled-Octupos-FullStack`

## Purpose

- This file is a human audit and navigation map behind the lightweight `SKILL.md` facade.
- Runtime models must not treat this markdown file as the primary rule source.
- Runtime routing must come from:
  - `python3 scripts/Cli_Toolbox.py skill-runtime-contract --json`
  - `python3 scripts/Cli_Toolbox.py skill-facade-contract --json`

## Runtime First

- Load the CLI JSON contracts first.
- Use this file only when a human or an audit flow needs a readable path map.
- If markdown and CLI JSON appear to differ, CLI JSON wins for runtime execution.

## Audit Navigation

- [顶层规则](../../rules/FULLSTACK_SKILL_HARD_RULES.md)
- [运行合同审计版](../runtime/SKILL_RUNTIME_CONTRACT.md)
- [项目统一目标基线](10_PROJECT_BASELINE_INDEX.md)
- [workflow contract](../tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md)
- [authored domains 索引](../authored_domains/00_DOMAIN_INDEX.md)
- `<root>/AGENTS.md`

## Project Baseline Entry

- [项目统一目标基线索引](10_PROJECT_BASELINE_INDEX.md)
- `mother_doc`、`implementation`、`evidence` 在进入具体容器或域前，先读取这层项目基线。
- `mother_doc` 的影响面判断固定采用：默认全相关，再按高概率不相关域做减法。

## Stage Entry

- `mother_doc`
  - [阶段说明](../stages/MOTHER_DOC_STAGE.md)
  - [子分支入口](../mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md)
  - [direct writeback](../mother_doc/DIRECT_WRITEBACK_BRANCH.md)
  - [question backfill](../mother_doc/QUESTION_BACKFILL_BRANCH.md)
  - [AGENTS branch](../mother_doc/agents_branch/00_BRANCH_INDEX.md)
  - [入口规则](../mother_doc/MOTHER_DOC_ENTRY_RULES.md)
  - [回填规则](../mother_doc/MOTHER_DOC_WRITEBACK_RULES.md)
- `implementation`
  - [阶段说明](../stages/IMPLEMENTATION_STAGE.md)
  - [交付规则](../implementation/IMPLEMENTATION_DELIVERY_RULES.md)
  - [对齐规则](../implementation/DOC_CODE_ALIGNMENT_RULES.md)
- `evidence`
  - [阶段说明](../stages/EVIDENCE_STAGE.md)
  - [evidence 索引](../evidence/00_EVIDENCE_INDEX.md)
  - [graph 子域入口](../evidence/graph/00_GRAPH_INDEX.md)
  - [OS_graph 规则](../evidence/OS_GRAPH_RULES.md)
  - [OS_graph 四层模型](../evidence/OS_GRAPH_LAYER_MODEL.md)
  - [doc-code 绑定规则](../evidence/DOC_CODE_BINDING_RULES.md)
  - [implementation 日志规则](../evidence/IMPLEMENTATION_LOG_RULES.md)
  - [deployment 日志规则](../evidence/DEPLOYMENT_LOG_RULES.md)

## Domain Entry

- `mother_doc` family
  - [writing rules](../authored_domains/mother_doc/WRITING_RULES.md)
  - [implementation rules](../authored_domains/mother_doc/IMPLEMENTATION_RULES.md)
  - [dev canon scope](../authored_domains/mother_doc/DEV_CANON_AUTOMATION_SCOPE.md)
- `ui` family
  - [writing rules](../authored_domains/ui/WRITING_RULES.md)
  - [implementation rules](../authored_domains/ui/IMPLEMENTATION_RULES.md)
  - [dev canon scope](../authored_domains/ui/DEV_CANON_AUTOMATION_SCOPE.md)
- `gateway` family
  - [writing rules](../authored_domains/gateway/WRITING_RULES.md)
  - [implementation rules](../authored_domains/gateway/IMPLEMENTATION_RULES.md)
  - [dev canon scope](../authored_domains/gateway/DEV_CANON_AUTOMATION_SCOPE.md)
- `service` family
  - [writing rules](../authored_domains/service/WRITING_RULES.md)
  - [implementation rules](../authored_domains/service/IMPLEMENTATION_RULES.md)
  - [dev canon scope](../authored_domains/service/DEV_CANON_AUTOMATION_SCOPE.md)
- `data_infra` family
  - [writing rules](../authored_domains/data_infra/WRITING_RULES.md)
  - [implementation rules](../authored_domains/data_infra/IMPLEMENTATION_RULES.md)
  - [dev canon scope](../authored_domains/data_infra/DEV_CANON_AUTOMATION_SCOPE.md)

## Tool Entry

- [Cli_Toolbox 入口](../../scripts/Cli_Toolbox.py)
- [容器骨架模块](../../scripts/container_scaffold.py)
- [Mother_Doc 导航模块](../../scripts/mother_doc_navigation.py)
- [Mother_Doc AGENTS/README 管理模块](../../scripts/mother_doc_agents_manager.py)
- [阶段合同支持模块](../../scripts/stage_contract_support.py)
- [OS_graph CLI](../../scripts/os_graph_cli.py)

## Lookup Hints

- Runtime model path:
  - first load `skill-runtime-contract`
  - then load `skill-facade-contract`
  - then descend into stage-level CLI contracts
- Human audit path:
  - use the indexes and links below to inspect the authored markdown structure
- If you need actual product-side authored content, move from the skill into `Octopus_OS/Mother_Doc/docs/<Container_Name>/`.
- `<root>` is the only product path anchor. Resolve real authored content as `<root>/Octopus_OS/Mother_Doc/docs/<Container_Name>/`.
