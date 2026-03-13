---
name: Meta-github-operation
description: 受限 GitHub control plane：仅服务 Octopus_OS 与 Otctopus_OS_AgentConsole 两个仓库的状态、提交、推送、远端信息与开发/发布分流约束。
metadata:
  doc_structure:
    doc_id: meta_github_operation.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Meta-github-operation skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Meta-github-operation

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Meta-github-operation/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## Status

本技能已恢复为受限启用状态，但当前只服务以下两个仓库：
- `/home/jasontan656/AI_Projects/Octopus_OS`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole`

本技能当前是按产品安装后的 repo 形态、远端命名与权限模型配置的受管 Git control plane：
- 默认同时覆盖私有开发远端与公开发布远端的治理约束
- 其中 `Otctopus_OS_AgentConsole` 已纳入开源发布仓 `public-release` 的管理位，但当前仍保持禁推
- 若其他用户希望复用本技能，应将 registry、repo 根、remote 命名、可写策略与权限前提改造成自己机器上的目标形态；AI 可以直接基于当前技能结构继续修改

对于 `Octopus_OS`：
- `origin`: 私有主远端 `Octopus_OS`
- 仓库名应与本地仓库名保持一致
- 预期保持闭源 / private
- bootstrap 时需要先补齐常用本地忽略项，再完成远端关联与首次/补推

对于 `Otctopus_OS_AgentConsole`，当前已进入双远端模型：
- `origin`: 私有开发仓 `Otctopus_OS_AgentConsole_AI_dev`
- `public-release`: 公开发布仓 `Otctopus_OS_AgentConsole`

当前策略：
- 自动迭代、同回合 Git traceability、日常 `commit-and-push` 只允许走 `origin`
- `message` 默认必须写成开发日志向 commit message，而不是只有一句短标题；至少应交代本次解决了什么问题、降低了什么风险或带来了什么行为变化
- 所有 remote write 动作必须串行执行，禁止并行 push / commit-and-push / baseline remote publish / repo-bootstrap push，避免撞上远端或宿主机 Git 锁
- `public-release` 只保留为未来发布用途
- 当前阶段禁止向 `public-release` 推送
- 禁用原因：
  - 开发尚未闭环到可发布状态
  - 发布流程尚未设计完成

## Scope

- 允许：
  - repo registry
  - status / remote-info
  - repo-bootstrap
  - fetch / pull-rebase
  - push-contract
  - baseline-contract
  - commit / commit-and-push / push
  - baseline-create
  - rollback-contract
  - rollback-paths
  - rollback-sync
- 不允许：
  - 超出上述两个仓库的 Git / GitHub 自动化调用
  - 对 `Otctopus_OS_AgentConsole/public-release` 的任何写入式 push 自动化
  - 仓库删除
  - 整个 workspace 根目录级 Git 操作

## Entry

- CLI 入口：`scripts/Cli_Toolbox.py`
- registry 固定只暴露：
  - `Octopus_OS`
  - `Otctopus_OS_AgentConsole`
- `remote-info` 与 `push-contract` 应成为 remote policy 的主读取入口
- `repo-bootstrap` 负责私有仓远端创建/校验、origin 关联、常用忽略项补齐以及首次/补推。
- 与运行时落盘/结果落点相关的 machine-readable 合同，应以 `push-contract --json`、`baseline-contract --json` 与 `rollback-contract --json` 返回的 `runtime_governance` 字段为准
- push 串行锁目录应以 `runtime_governance.push_lock_dir` 为准；需要 remote write 时必须使用受管锁，不得并行触发多个 push

## Runtime And Output Governance

- 技能 runtime 根目录：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/meta-github-operation`
- thread-owned claims 目录：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/meta-github-operation/claims`
- 兼容回退读取：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`
- 技能 result 根目录：
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/meta-github-operation`
- 当前默认行为：
  - CLI 以 stdout JSON 为主，不持久化滚动日志文件。
  - 若使用 `--use-latest-claims`，应优先读取 namespaced claims 目录；legacy root 仅保留兼容读取，不再作为首选落点。
  - 若未来新增文件型结果或审计导出，必须要求显式目标路径，或默认落入受管 result 根目录。
  - remote write 相关命令会在 namespaced push lock 目录下获取 repo 级串行锁。
- 历史迁移责任：
  - 旧的 `Meta-github-operation_thread_owned_paths*.json*` 若仍散落在 `Codex_Skill_Runtime` 根目录，应整理迁移到 namespaced claims 目录。

## Remote Policy

- `Octopus_OS`
  - `origin`
    - 角色：private primary remote
    - 用途：闭源主远端、常规迭代、首次/补推 bootstrap
    - 写入策略：允许
    - 附加约束：
      - 远端仓库名应与本地仓库名一致
      - 默认保持 private
      - bootstrap 前应补齐日志、临时文件、虚拟环境、缓存目录、`.env` / `.env.example` 等常用忽略项
- `Otctopus_OS_AgentConsole`
  - `origin`
    - 角色：private development traceability remote
    - 用途：自动迭代、开发日志、同回合 push
    - 写入策略：允许
  - `public-release`
    - 角色：future public release remote
    - 用途：未来人工选择稳定快照后发布
    - 写入策略：当前禁用
    - 禁用原因：开发未闭环至可发布；发布流程尚未设计

## Current Delivery Rule

- 若用户要求为 `Octopus_OS` 新建或校验闭源远端，优先走 `repo-bootstrap`，并默认使用 private visibility。
- 若用户要求正常提交并推送 `Otctopus_OS_AgentConsole`，默认只推 `origin`
- 若用户要求 `commit` / `commit-and-push` / `repo-bootstrap --message`，message 必须写成开发日志向风格，至少包含标题和两条以上细节，并明确说明本次解决的问题或影响
- 若用户明确要求发布到公开仓，必须先声明当前禁用，再解释原因
- 在发布流程尚未设计完成前，不得把 `public-release` 当成可写远端偷偷使用

## Reactivation Boundary

- 这是 GitHub 重构后的第一阶段恢复。
- 若未来要支持更多仓库，必须先扩 registry 与 AGENTS 绑定，再扩工具面。
