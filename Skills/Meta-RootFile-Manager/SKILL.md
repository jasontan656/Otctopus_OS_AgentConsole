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
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<governed external path>" --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 工具入口
- 本技能提供可执行 CLI：
  - `scaffold`
  - `scan`
  - `lint`
  - `collect`
  - `push`
  - `target-contract`
- 所有写操作类命令必须支持 `--dry-run`。
- 工具行为必须服从 `references/runtime_contracts/` 下的静态治理合同。

## 2. 受管模型
- 本技能不再限制为 markdown。
- 本技能治理的是 workspace 内各 repo root 或 workspace root 的默认受管文件。
- 每一种文件类型都必须有独立 `channel`。
- 每个 `channel` 可以治理多个外部路径。
- 当前 channel 注册表以 [rules/scan_rules.json](rules/scan_rules.json) 为真源。

## 3. 通道语义
- `AGENTS_MD`
  - 仍使用 `Part A / Part B` 双承载治理模型。
  - 内部治理映射由 `AGENTS_human.md + AGENTS_machine.json` 共同组成。
  - `owner` 必须进入 external/internal human frontmatter、machine payload 与 owner meta。
- 其他 root file channel
  - 不使用 `A/B` 分段。
  - 技能内部保存“外部文件内容的治理映射版本”。
  - 映射版本文件名必须显式带有 `__governed_external` 语义，避免与外部真实文件同名导致误扫描。
  - 所有受管 target 都必须额外生成一个 owner meta 文件。
  - 对可人类直读的 markdown channel，内部映射版本必须显式带 `owner` 字段，便于直接阅读时知道“谁是它的爹、受谁治理”。
  - `owner` 的值不是固定枚举，而是根据受管目录语义自动推导出的描述性内容。

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

## 6. 参考入口
- [AGENTS 资产治理模型](references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md)
- [AGENTS 结构合同](references/runtime_contracts/AGENTS_content_structure.md)
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
- `collect` 必须以外部源为真源覆盖技能内映射。
- `push` 必须以技能内映射为真源覆盖外部目标。
