# AGENTS.md - Octopus CodeBase Backend

[OCTOPUS_BACKEND_CODEBASE_CONTRACT - HARD ENFORCEMENT]

0) Scope (Required)
- 本文件只约束：`/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend` 这个后端 codebase 仓库。
- 本文件是 `3-Octupos-OS-Backend` 技能在 codebase 侧的执行合同。
- 根工作区运行钩子、stage guardrails、push/lint 总规则仍由：`/home/jasontan656/AI_Projects/AGENTS.md` 负责。
- 后端技能主合同仍由：`/home/jasontan656/.codex/skills/3-Octupos-OS-Backend/SKILL.md` 负责。

1) Role Split (Required)
- `3-Octupos-OS-Backend` 负责：`mother_doc -> construction_plan -> implementation -> acceptance` 四阶段总控。
- 本 AGENTS 只负责 codebase 侧提醒：
  - 代码必须受 construction plan 约束
  - 设计意图来自 mother doc 内的设计者规划，而不是来自代码自身
  - 代码必须来自 requirement atoms 映射
  - 测试与真实 witness 不能伪造
  - 本仓只放业务代码、测试、运行入口、部署脚本
- 本仓不接受技能主合同之外的自造 gate/report/task-stack 工件要求。

1.1) Resident Vs Stage Docs (Required)
- 跨阶段只允许常驻：
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend/AGENTS.md`
  - `3-Octupos-OS-Backend` 的硬规则与 workflow contract
- 阶段专属读物边界、命令和 graph 角色应直接读取 skill 的 `stage-doc-contract`、`stage-command-contract`、`stage-graph-contract` 输出，而不是从正文长文里自行重建。
- 进入 `implementation` 时，只保留 implementation 当前需要的 mother doc 章节、当前 active pack、当前 inner phase 所需 codebase 文件。
- 切换到 `acceptance` 时，必须丢弃 implementation 局部调试 focus、非证据化临时笔记、未激活 pack 的施工语义；若 acceptance 需要某条实现信息，必须以 evidence ref 或 active pack 回写结果重新引入。

2) Source Of Truth (Required)
- 唯一需求源固定为：`/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/docs/mother_doc/`
- design phase plan、Execution_atom_plan&validation_packs、ADR 文档固定收敛在：`/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/docs/mother_doc/`；`acceptance report` 与 `acceptance matrix` 固定收敛在：`/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/docs/mother_doc/acceptance/`。
- 本仓不得把 Human_Work_Zone 或任意非合同 runtime 工件当成需求源。

3) Implementation Entry Guard (Required)
- 在本仓开始写代码前，必须已经存在：
  - directory mother doc
  - requirement atom inventory
  - mother doc 内的 design phase plan
  - `docs/mother_doc/execution_atom_plan_validation_packs/`
  - baseline_mode 判断
  - blocked_state 判断
- 若缺上述任一项，不得直接开始 implementation。
- 进入 implementation 前，必须显式读取当前阶段 checklist；不得继续沿用 mother_doc 或 construction_plan 阶段的旧 checklist/focus。
- 若 implementation 与 active pack 偏离，必须先回写 runtime 中 `docs/mother_doc/execution_atom_plan_validation_packs/` 对应 pack 目录下的 machine files 与 markdown anchors，再继续改代码；若设计意图变化，再同步回写 mother doc 内的 design phase plan。

4) Codebase Boundaries (Required)
- 本仓固定承载：
  - backend application code
  - tests
  - config templates
  - migrations
  - deployment/unit files
  - executable runtime entrypoints
- 本仓不得承载：
  - mother doc 主文档
  - design phase plan 主文档
  - execution packs 主文档
  - acceptance report 主文档
  - acceptance matrix 主文档
  - code graph runtime 产物
- 图谱由独立技能 `Meta-code-graph-base` 生成，产物固定落在 runtime；本仓只在 `mother_doc`/`construction_plan` 上游阶段消费其上下文，不在 implementation 阶段把它当主读物，也不内建图谱生成逻辑。
- acceptance/evidence 收口后可以更新图谱，但图谱更新不构成 codebase 自身的验收证据。

5) Environment And Commands (Required)
- Python 虚拟环境固定为：`/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend/.venv-wsl`
- 依赖安装、代码执行、测试命令必须在该虚拟环境下运行。
- 本地开发与 acceptance 默认直接读取 `/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend/.env.example` 作为非 Git secrets source；该文件已预置两个生产测试 bot token 与模型目标 `gpt-5.4 reasoning effort high`，后续开发机器人应直接消费，不得把 token 回写进 mother doc、runtime 文档或任何可推送文件。
- `README.md` 与 `Deployment_Guide.md` 若声明了启动/部署命令，命令必须可实跑；失效命令必须随代码一并修正。
- 若 systemd/unit/ngrok/webhook 配置与当前代码不一致，不得忽略，必须一起修到可运行状态或显式进入 `needs_real_env`。

6) Behavior Contract (Required)
- 代码实现必须能映射回 `requirement_atom_id`。
- 测试必须断言需求行为，不得只断言占位字段、feature_id、status 字符串或自造 report。
- 禁止使用最小伪实现冒充生产实现，特别是：
  - stub service
  - fake witness
  - in-memory authority source
  - self-authored completion report
- 缺真实环境、缺凭据、缺外部系统可达性时，必须进入 `blocked_state`，不得宣称闭环完成。

7) Acceptance Contract (Required)
- 本仓完成 implementation 后，必须至少具备：
  - code 落盘
  - tests 落盘并实跑
  - 运行入口可执行
  - 对应真实 witness 获取路径明确
- `acceptance` 必须继续把本地可控配置真正配好：读取本地 ignored env/secrets source、补齐 token/webhook secret/owner allowlist/runtime endpoint、拉起 resident services、做至少一轮模拟人类使用，并把这些结果回写成真实 witness。
- 只有当以上本地 bring-up 已经穷尽且仍缺外部条件时，才允许写 `needs_real_env`。
- 最终完成态只能由 runtime 中 `docs/mother_doc/acceptance/` 下的 acceptance report + acceptance matrix 裁决，不由本仓单独裁决。

8) Maintenance Sync (Required)
- 只要 `3-Octupos-OS-Backend` 技能的阶段、模板、合同对象发生变化，必须同步检查：
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend/AGENTS.md`
- 目标是保证：
  - 根 AGENTS 不与技能主合同冲突
  - codebase AGENTS 只描述当前 backend workflow 合同
- 若技能已更新而本 AGENTS 仍偏离当前 workflow 合同，判定为 `violation`。
