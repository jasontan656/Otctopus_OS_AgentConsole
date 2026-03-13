---
name: Meta-RootFile-Manager
description: 集中管理 workspace 内的根级默认受管文件。当前提供 scan / lint / collect / push / scaffold / target-contract CLI，并按文件类型通道治理多个外部路径。
metadata:
  doc_structure:
    doc_id: meta_rootfile_manager.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Meta-RootFile-Manager skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Meta-RootFile-Manager

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 工具入口
- 本技能提供可执行 CLI：
  - `contract`
  - `scaffold`
  - `scan`
  - `lint`
  - `collect`
  - `push`
  - `target-contract`
  - `agents-payload-contract`
- 所有写操作类命令必须支持 `--dry-run`。
- 工具行为必须服从 `references/runtime_contracts/` 下的静态治理合同。

## 2. 受管模型
- 本技能不再限制为 markdown。
- 本技能治理的是 workspace 内各 repo root 或 workspace root 的默认受管文件。
- 每一种文件类型都必须有独立 `channel`。
- 每个 `channel` 可以治理多个外部路径。
- 当前 channel 注册表以 [rules/scan_rules.json](rules/scan_rules.json) 为真源。

## 3. 通道语义
- `channel` 只表达文件类型级治理差异。
- 每个 `channel` 必须声明自己的 `mapping_mode` 与对应的内部承载形态。
- channel 专属的结构合同、payload 工作流、例外约束与专用入口，必须下沉到各自的治理入口或下游 runtime contract，不在本章展开。
- 通用映射承载与 `owner` 写入规则，以 runtime contract 与下游结构合同为准。

## 4. 当前已开通文件类型
- `AGENTS.md`
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE`
- `.gitignore`
- `pytest.ini`
- `Dockerfile`
- `.dockerignore`
- `.env.example`
- `requirements.txt`
- `requirements-backend_skills.lock.txt`
- `pyproject.toml`
- `package.json`
- `package-lock.json`

## 5. 阶段阅读入口
- `scaffold`
  - 说明：在外部目标目录创建第一版 root file，并同时创建技能内治理映射。
  - 阅读入口：`references/runtime_contracts/SCAFFOLD_STAGE_CONTRACT.md`
- `new-file`
  - 说明：为新的 root file 类型开通独立 channel，并定义其内部映射承载命名。
  - 阅读入口：`references/runtime_contracts/NEW_FILE_STAGE_CONTRACT.md`
- `scan`
  - 说明：按 channel 注册表发现当前已经受管的外部目标。
  - 阅读入口：`references/runtime_contracts/SCAN_STAGE_CONTRACT.md`
- `collect`
  - 说明：把外部真源回收覆盖到技能内部映射版本。
  - 阅读入口：`references/runtime_contracts/COLLECT_STAGE_CONTRACT.md`
- `push`
  - 说明：把技能内部映射版本覆盖回外部目标。
  - 阅读入口：`references/runtime_contracts/PUSH_STAGE_CONTRACT.md`
- `agents-payload-contract`
  - 说明：治理 `AGENTS_machine.json` payload 的专用入口合同。
  - 强制工作流：`$Meta-Enhance-Prompt 提取用户意图 -> 压缩为最小精确语义 -> 回写 AGENTS_machine.json -> collect 重渲染 AGENTS_human.md -> lint`
  - 阅读入口：`references/runtime_contracts/AGENTS_GOVERNANCE_ENTRY.md`

## 6. 参考入口
- [AGENTS 治理入口](references/runtime_contracts/AGENTS_GOVERNANCE_ENTRY.md)
- [Root File 映射副本合同](references/runtime_contracts/ROOTFILE_MAPPED_COPY_STRUCTURE.md)
- [技能运行合同](references/runtime_contracts/SKILL_RUNTIME_CONTRACT.md)
- [新增文件类型合同](references/runtime_contracts/NEW_FILE_STAGE_CONTRACT.md)
- [Scan 阶段合同](references/runtime_contracts/SCAN_STAGE_CONTRACT.md)
- [Collect 阶段合同](references/runtime_contracts/COLLECT_STAGE_CONTRACT.md)
- [Push 阶段合同](references/runtime_contracts/PUSH_STAGE_CONTRACT.md)
- [当前受管资产根目录](assets/managed_targets/AI_Projects)

## 7. 约束
- 项目技能只声明哪些 root file 必须存在，不负责这些默认文件的长期正文维护。
- 默认文件正文的回收与推出必须通过本技能完成，避免单点直接编辑导致治理链断裂。
- `scan` 规则必须外置在 `rules/scan_rules.json`，不得把 channel 注册表重新硬编码进 CLI。
- 非 `AGENTS.md` 文件的技能内映射文件不得与外部真实文件同名。
- `target-contract`、`scan`、`collect`、`push`、`scaffold` 的输出都必须暴露 `owner`。
- `AGENTS_machine.json` payload 变更不得绕过 `agents-payload-contract` 入口合同。
- `collect` 必须以外部源为真源覆盖技能内映射。
- `push` 必须以技能内映射为真源覆盖外部目标。
