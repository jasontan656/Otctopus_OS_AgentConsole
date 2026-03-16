---
name: Meta-RootFile-Manager
description: 集中管理 workspace 内的根级默认受管文件。当前提供 scan / lint / collect / push / scaffold / target-contract 等 CLI，并按文件类型通道治理多个外部路径。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
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
- CLI JSON is the runtime source; `SKILL.md` 只保留入口门面与路由摘要。

## 1. 工具入口
- 本技能提供以下主要命令：
  - `contract`
  - `scan`
  - `lint`
  - `collect`
  - `push`
  - `scaffold`
  - `new-writeback`
  - `target-contract`
  - `agents-maintain`
  - `agents-domain-contract`
  - `agents-payload-contract`
- 所有写操作类命令必须支持 `--dry-run`。

## 2. 通道模型
- 本技能治理 workspace 内各 repo root 或 workspace root 的默认受管文件。
- 每一种文件类型都必须有独立 `channel`。
- `channel` 只表达文件类型级差异，不承载动态 governed target 注册。
- 当前静态 channel 规则以 `rules/scan_rules.json` 为真源。

## 3. AGENTS 当前治理形态
- 外部 `AGENTS.md` 可见面本身就是完整成立的 runtime hook contract。
- `Part A` 固定拆为：
  - `<contract>`
  - `<reminder>`
- `contract` 承载第一眼可见的强约束、入口命令与路由。
- `reminder` 只承载提醒，不得混入硬合同语气。
- 内部 `AGENTS_human.md` 是唯一真源，并在 `<part_B>` 中承载多个分域 `json` block。
- 每个分域 block 必须独立携带：
  - `domain_id`
  - `read_command_preview`
  - `contract`

## 4. AGENTS 维护主链
- 日常 AGENTS 维护统一入口是 `agents-maintain`。
- 主链固定为：
  - 自然语言意图
  - target ranking
  - contract surface / domain block placement
  - ancestor / duplicate gate
  - update `AGENTS_human.md`
  - centered push external `AGENTS.md`
  - lint
- `collect` 对 `AGENTS.md` 只保留 reverse-sync / recovery 语义，不再属于日常闭环。

## 5. AGENTS 狭义入口
- `target-contract`
  - 输出目标整体合同、managed truth source 与分域读取入口。
- `agents-domain-contract`
  - 输出单个分域 machine contract。
- `agents-payload-contract`
  - 历史命名保留入口；现在只处理已知目标上的分域 block surgery。

## 6. 强门禁
- `lint` 必须拦截：
  - 外部 `AGENTS.md` 泄露 frontmatter 治理元信息或 `<part_A>` 内部装配壳
  - 外部可见合同面缺失 `<contract>` 或 `<reminder>`
  - 外部可见合同面不是“完整合同正文后接 reminder 尾部”的纯结构
  - reminder 中混入 `必须`、`不得`、`must`、`shall` 等硬合同语气
  - `Part B` 缺域、重域、无 `domain_id`、非 `json` 内容
  - 父子 AGENTS 语义重复
  - payload block 中出现技能顺序、repo 摘要、技术栈清单、Markdown 叙事等软语义
  - repo-tracked orphan AGENTS 映射、installed drift 与 runtime legacy sidecar 残留

## 7. 运行与资产约束
- `push` 必须以技能内映射为真源覆盖外部目标。
- runtime 日志、latest 结果、临时镜像与缓存产物必须落在 `Codex_Skill_Runtime/<skill>/...`。
- workspace 外部源路径或临时工作区源路径必须按 runtime-local 处理，不得在 repo-tracked `assets/managed_targets/...` 下制造临时目录。

## 8. 参考入口
- `references/runtime_contracts/AGENTS_GOVERNANCE_ENTRY.md`
- `references/runtime_contracts/AGENTS_content_structure.md`
- `references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md`
- `references/runtime_contracts/AGENTS_payload_structure_human.md`
- `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.md`
- `assets/managed_targets/AI_Projects`
