---
name: Meta-github-operation
description: AI 主动使用的 runtime hook GitHub control plane：仅服务 Octopus_OS 与 Otctopus_OS_AgentConsole 两个仓库，并治理 traceable record repo 与人类显式门禁 remote 的写入边界。
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

## Default Use Mode

- 本技能是 AI 默认主动使用的 runtime hook Git traceability skill，不是只在用户点名时才触发的手动 Git 工具。
- 只要任务进入 `Octopus_OS` 或 `Otctopus_OS_AgentConsole` 且出现 commit / push / remote policy / traceability 需求，AI 应主动进入本技能。
- 技能内部再区分两类 remote：
  - AI traceable record remote：默认给 AI 日常自动使用
  - human-controlled remote：只有人类显式要求时才允许使用


## Status

本技能已恢复为受限启用状态，但当前只服务以下两个仓库：
- `/home/jasontan656/AI_Projects/Octopus_OS`
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole`

本技能当前是按产品安装后的 repo 形态、远端命名与权限模型配置的受管 Git control plane：
- 默认覆盖 AI traceable record remote 与 human-controlled remote 两类写入面
- 其中 `Otctopus_OS_AgentConsole` 已纳入开源发布仓 `public-release` 的管理位，但该远端只允许在人类显式要求时推送
- 若其他用户希望复用本技能，应将 registry、repo 根、remote 命名、可写策略与权限前提改造成自己机器上的目标形态；AI 可以直接基于当前技能结构继续修改

对于 `Octopus_OS`：
- `origin`: AI 日常私有远端 `Octopus_OS_AI`
- `human-sync`: 人类显式触发私有远端 `Octopus_OS_humen`
- 预期保持闭源 / private
- `origin` 只给 AI 日常推送使用
- `human-sync` 只有在人类显式要求推送时才允许使用
- bootstrap 时需要先补齐常用本地忽略项，再完成远端关联与首次/补推

对于 `Otctopus_OS_AgentConsole`，当前已进入双远端模型：
- `origin`: 私有 AI 开发仓 `Otctopus_OS_AgentConsole_AI_dev`
- `public-release`: 公开发布仓 `Otctopus_OS_AgentConsole`

当前策略：
- AI 自动迭代、同回合 Git traceability、日常 `commit-and-push` 默认走 traceable record remote
- `message` 默认必须写成开发日志向 commit message，而不是只有一句短标题；至少应交代本次解决了什么问题、降低了什么风险或带来了什么行为变化
- 所有 remote write 动作必须串行执行，禁止并行 push / commit-and-push / baseline remote publish / repo-bootstrap push，避免撞上远端或宿主机 Git 锁
- `human-sync` 与 `public-release` 都属于人工门禁远端
- 这类 remote 默认禁止自动写入；只有当人类显式要求时，才允许通过受管 CLI 加 `--human-explicit-request` 推送

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
  - 对任何人工门禁 remote 的隐式自动推送
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
- 技能 result 根目录：
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/meta-github-operation`
- 当前默认行为：
  - CLI 以 stdout JSON 为主，不持久化滚动日志文件。
  - 若使用 `--use-latest-claims`，只读取 namespaced claims 目录。
  - 若未来新增文件型结果或审计导出，必须要求显式目标路径，或默认落入受管 result 根目录。
  - remote write 相关命令会在 namespaced push lock 目录下获取 repo 级串行锁。
- 历史迁移责任：
  - 旧的 `Meta-github-operation_thread_owned_paths*.json*` 若仍散落在 `Codex_Skill_Runtime` 根目录，应直接移除或手动迁入 namespaced claims 目录；当前运行面不再兼容读取旧根目录。

## Remote Policy

- `Octopus_OS`
  - `origin`
    - 角色：private AI daily remote
    - 用途：闭源 AI 日常迭代、首次/补推 bootstrap、traceable record
    - 写入策略：允许
    - 附加约束：
      - 远端仓库名固定为 `Octopus_OS_AI`
      - 默认保持 private
      - bootstrap 前应补齐日志、临时文件、虚拟环境、缓存目录、`.env` / `.env.example` 等常用忽略项
  - `human-sync`
    - 角色：private human explicit remote
    - 用途：闭源人工镜像 / 人类显式触发推送
    - 写入策略：仅人类显式要求时允许
    - 附加约束：
      - 远端仓库名固定为 `Octopus_OS_humen`
      - 默认保持 private
- `Otctopus_OS_AgentConsole`
  - `origin`
    - 角色：private AI daily remote
    - 用途：自动迭代、开发日志、同回合 push、traceable record
    - 写入策略：允许
    - 附加约束：
      - 远端仓库名固定为 `Otctopus_OS_AgentConsole_AI_dev`
  - `public-release`
    - 角色：human explicit public release remote
    - 用途：开源发布仓，只在人类显式要求时推送
    - 写入策略：仅人类显式要求时允许

## Current Delivery Rule

- 若用户要求为 `Octopus_OS` 新建或校验闭源远端，优先走 `repo-bootstrap`，并默认使用 private visibility。
- 若任务需要 AI 正常提交并推送 `Octopus_OS` 或 `Otctopus_OS_AgentConsole`，默认走各自的 `origin` traceable record remote
- 若用户要求推 `Octopus_OS/human-sync` 或 `Otctopus_OS_AgentConsole/public-release`，必须是显式人工请求，并且调用时必须加 `--human-explicit-request`
- 若用户要求 `commit` / `commit-and-push` / `repo-bootstrap --message`，message 必须写成开发日志向风格，至少包含标题和两条以上细节，并明确说明本次解决的问题或影响
- 不得把人工门禁 remote 当成默认可写远端偷偷使用

## Reactivation Boundary

- 这是 GitHub 重构后的第一阶段恢复。
- 若未来要支持更多仓库，必须先扩 registry 与 AGENTS 绑定，再扩工具面。
