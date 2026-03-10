# Mother_Doc AGENTS/README Branch Contract

## Contract Header
- `contract_name`: `2_octupos_fullstack_references_mother_doc_agents_branch_runtime_agents_branch_contract`
- `contract_version`: `2.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

适用阶段：`mother_doc`

## Runtime Source Policy

- 主运行时来源：`python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- 阶段指令：`python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
- 机器索引：`python3 scripts/Cli_Toolbox.py mother-doc-agents-registry --json`
- 具体路径合同：`python3 scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "<PATH>" --file-kind <agents|readme> --json`
- `CLI JSON` 是 runtime 主源；审计 markdown 与路径索引都不是主运行时指令。
- `00_BRANCH_INDEX.md` 与 `assets/mother_doc_agents/index.md` 都只保留人类导航 / 审计角色，不再作为模型主运行时入口。

## Scope

- 管理 3 类路径：
  - `Octopus_OS/AGENTS.md + README.md`
  - `Octopus_OS/<Container_Name>/AGENTS.md + README.md`
  - `Octopus_OS/Mother_Doc/docs/**/AGENTS.md + README.md`
- 不管理实际工作目录容器。
- 不管理普通正文文档。

## Fixed Stages

- `scan`: 扫描当前 AGENTS/README 树现状。
- `collect`: 把当前 AGENTS/README 树反向采集回技能侧 registry。
- `push`: 从技能侧模板反推整棵 AGENTS/README 树，并刷新 registry。

## Template Semantics

- `治理映射模版`
  - 定义：skill 内长期保存、会被 `collect / push` 持续读写的被治理文件映射层。
  - 资产包含：
    - `assets/mother_doc_agents/runtime_rules/**/**/*.runtime.json`
    - `assets/mother_doc_agents/runtime_rules/**/AGENT_AUDIT.md`
    - `assets/mother_doc_agents/runtime_rules/**/README_AUDIT.md`
    - `assets/mother_doc_agents/collected_tree/**/AGENTS.md`
    - `assets/mother_doc_agents/collected_tree/**/README.md`
    - `assets/mother_doc_agents/templates/**/AGENTS.md`
    - `assets/mother_doc_agents/templates/**/README.md`
  - 真源边界：
    - `collect` 把外部当前态收敛进来覆盖对应治理映射资产。
    - `push` 再把 skill 内治理映射资产作为内部真源推回外部目标。
    - 对 `AGENTS` 而言，`runtime_rules JSON` 承载运行时主源；对 `README` 而言，`template/collected snapshot + registry` 共同承载当前态映射。
- `骨架生成模版`
  - 定义：用于初始化新目标或补齐缺失导航文件的默认骨架生成规则。
  - 当前归属在 `build_octopus_root_agents`、`build_container_root_agents` 与 `sync_navigation_tree`。
  - 真源边界：
    - 它只负责产出第一版外部骨架与第一版内部映射资产。
    - 一旦目标进入 `collect / push` 周期，长期语义回到 `治理映射模版`。

## Managed Asset Model

- 外部 `AGENTS.md`
  - 形态：`thin_runtime_entry_only`
  - 运行主源：`assets/mother_doc_agents/runtime_rules/**/AGENTS.runtime.json`
  - 审计副本：`assets/mother_doc_agents/runtime_rules/**/AGENT_AUDIT.md`
- 外部 `README.md`
  - 形态：`human_summary_only`
  - `Octopus_OS` 根层与容器根：`template_managed`
  - `Mother_Doc/docs/**/README.md`：`collect_preserve`

## Forbidden Runtime Pattern

- 不要把审计 markdown 路径当成主运行时指令。
- 不要要求模型为了知道下一步动作而继续追一串 markdown。
- 不要只给路径元数据而不给直接动作指导。

## Branch Profiles

- `octopus_os_root`
  - `AGENTS.md` 是 workspace root runtime entry。
  - `README.md` 是 workspace root human summary。
- `container_roots`
  - `AGENTS.md` 是容器根 runtime entry。
  - `README.md` 是容器根 human summary。
- `mother_doc_docs`
  - `AGENTS.md` 是递归 doc scope runtime entry。
  - `README.md` 是当前层 human summary。

## Assets

- `assets/mother_doc_agents/scan_report.json`
- `assets/mother_doc_agents/registry.json`
- `assets/mother_doc_agents/index.md` (`human_audit_only`)
- `assets/mother_doc_agents/collected_tree/`
- `assets/mother_doc_agents/templates/`

## Branch Runtime Rules

- 先读 CLI JSON，再决定是否打开 markdown 审计版。
- 需要当前 managed target 列表时，优先使用 `mother-doc-agents-registry --json`，把 branch index 内容通过 JSON payload 提供。
- 需要具体路径动作指导时，优先使用 `mother-doc-agents-target-contract`。
- 本分支只负责 `mother_doc` 内部的 AGENTS/README 治理，不处理 implementation 或 evidence。
