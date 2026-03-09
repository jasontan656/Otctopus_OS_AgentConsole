# Cli_Toolbox 使用文档

适用技能：`2-Octupos-FullStack`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- `Cli_Toolbox.mother_doc_stage` -> `scripts/Cli_Toolbox.py mother-doc-stage`
- `Cli_Toolbox.materialize_container_layout` -> `scripts/Cli_Toolbox.py materialize-container-layout`
- `Cli_Toolbox.implementation_stage` -> `scripts/Cli_Toolbox.py implementation-stage`
- `Cli_Toolbox.evidence_stage` -> `scripts/Cli_Toolbox.py evidence-stage`

## 叙事式使用说明（固定格式）

### Cli_Toolbox.materialize_container_layout
- 人类叙事版输入：
  - AI 已根据用户描述判定本项目需要哪些容器名称，例如 `User_UI`、`Admin_UI`、`Mongo_DB`。
- 电脑动作发生了什么：
  - 调用 `scripts/Cli_Toolbox.py materialize-container-layout`。
  - 在 `Octopus_OS/` 下创建同名容器目录。
  - 在 `Octopus_OS/Mother_Doc/` 下创建同名文档目录。
  - 为每个容器文档目录补齐 `README.md + common/` 的基础骨架。
  - 按容器族补齐 `common/architecture`、`common/stack`、`common/naming`、`common/contracts`、`common/operations` 下的 markdown 占位文件。
  - 若容器名是 `Mother_Doc`，则保留工作目录 `Octopus_OS/Mother_Doc/`，并确保自描述目录 `Octopus_OS/Mother_Doc/Mother_Doc/` 具备 `00_INDEX.md` 与完整 `common/` 骨架。
  - 若目录或文件已存在，则保持幂等。
- 人类叙事版输出：
  - 返回已创建目录、已存在目录、已创建文档文件与命名告警，便于继续写文档和落代码。

### Cli_Toolbox.mother_doc_stage
- 人类叙事版输入：
  - 需要进入 `mother_doc` 阶段并确认其作用域、必须加载的顶层规则、以及它产出什么。
- 电脑动作发生了什么：
  - 调用 `scripts/Cli_Toolbox.py mother-doc-stage`。
  - 输出 `mother_doc` 阶段的 scope、must_load、requires、produces。
- 人类叙事版输出：
  - 返回 `mother_doc` 阶段合同，供当前回合约束使用。

### Cli_Toolbox.implementation_stage
- 人类叙事版输入：
  - 需要进入 `implementation` 阶段并确认它必须显式承接哪些前序内容。
- 电脑动作发生了什么：
  - 调用 `scripts/Cli_Toolbox.py implementation-stage`。
  - 输出 `implementation` 阶段的 scope、must_load、requires、produces。
- 人类叙事版输出：
  - 返回 `implementation` 阶段合同，明确必须承接 `mother_doc` 产物。

### Cli_Toolbox.evidence_stage
- 人类叙事版输入：
  - 需要进入 `evidence` 阶段并确认它必须显式承接哪些前序内容。
- 电脑动作发生了什么：
  - 调用 `scripts/Cli_Toolbox.py evidence-stage`。
  - 输出 `evidence` 阶段的 scope、must_load、requires、produces。
- 人类叙事版输出：
  - 返回 `evidence` 阶段合同，明确必须承接 `mother_doc` 与 `implementation` 产物。

## 示例命令（强制）
- 最小用途描述：
  - 根据 AI 已判定的容器名，创建工作目录、`Mother_Doc` 同名目录，以及对应容器族的 `common/` 抽象层骨架。
- 一行命令（必须满足以下全部约束）：
  - 必须以 `cd <skill_root> &&` 开头。
  - 必须为“一行可复制”的完整命令。
  - 必须包含管道（例如 `| sed -n '1,200p'`）以便快速查看结果。
  - 命令必须能一键直达脚本预期参数并得到可复现输出。
- 示例：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py mother-doc-stage --json | sed -n '1,200p'`
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py materialize-container-layout --container Mother_Doc --container User_UI --container Mongo_DB --dry-run --json | sed -n '1,220p'`
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py implementation-stage --json | sed -n '1,200p'`
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py evidence-stage --json | sed -n '1,200p'`

## 参数与结果（供 AI/工程使用）
- 输入：
- `--workspace-root`
- `--document-root`
- `--container`（可重复）
- `--dry-run`
- `--json`
- 输出：
- `created_workspace_dirs`
- `created_document_dirs`
- `existing_workspace_dirs`
- `existing_document_dirs`
- `created_document_files`
- `warnings`
- 失败码约定：
- `0`: 成功
- `2`: 参数错误或命名错误

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若为多模块 Toolbox，还需同步更新：
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档（`references/tooling/development/modules/*.md`）
- 若工具承载运行态规则、约束、指引，还必须同步更新：
  - machine-readable 合同（`json/yaml`）
  - markdown 审计版
