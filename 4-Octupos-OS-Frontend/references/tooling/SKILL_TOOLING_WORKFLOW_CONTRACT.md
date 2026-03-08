# 4-Octupos-OS-Frontend Tooling & Workflow Contract

## Contract Header
- `contract_name`: `octopus_frontend_narrative_workflow_contract`
- `contract_version`: `3.1.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `stage_order`
  - `stage_objectives`
  - `discovery_scope_policy`
  - `phase_read_policy`
  - `requirement_atom_required_fields`
  - `baseline_mode_policy`
  - `blocked_state_policy`
  - `graph_preflight_policy`
  - `graph_postflight_policy`
  - `required_templates`
  - `design_phase_plan_required_sections`
  - `construction_plan_required_sections`
  - `acceptance_required_fields`
  - `acceptance_matrix_required_fields`
  - `adr_required_sections`
- `optional_fields`:
  - `example_commands`
  - `notes`

## 1. 定位
- 本合同定义章鱼 OS frontend skill 的四阶段项目说明驱动工作流。
- 图谱能力由 `Meta-code-graph-base` 提供；本合同只定义它在工作流中的位置。

## 1.1 Discovery Scope Policy
- 发现范围只允许包含：
  - `/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend`
  - `/home/jasontan656/AI_Projects/OctuposOS_RunTime_Frontend`
  - `/home/jasontan656/AI_Projects/OctuposOS_RunTime_Frontend/docs`
  - `/home/jasontan656/AI_Projects/OctuposOS_RunTime_Frontend/docs/mother_doc`
  - 当前技能文件与必要图谱技能入口
- 若启动 cwd 是 `/home/jasontan656/AI_Projects`，它只是容器根与钩子根，不是 discoverable repo。
- 禁止为了找需求或上下文而扫描整个 `/home/jasontan656/AI_Projects`。
- 禁止读取 `Human_Work_Zone`、`GoogleDriveDump` 等 sibling 区域，除非 mother doc 显式引用。
- 极简 prompt 启动时，第一批动作固定为：
  - 若需要则执行 `mother-doc-init`
  - 直接读取固定 `docs/mother_doc/00_index.md`
  - 若已存在编号归档的 `docs/NN_slug`，先读取最新一轮归档内容再开始本轮回填
  - 执行 `mother-doc-lint`
  - 若存在图谱，读取 graph context 以校准当前代码现实
  - 仅在当前阶段确实需要代码上下文时，执行固定 codebase 路径上的 `graph-preflight`
  - 仅在这些步骤后，按需读取 codebase 中的具体文件

## 1.2 Top-Level Resident Docs
- 跨四阶段唯一允许常驻的文档只有：
  - `rules/OCTOPUS_SKILL_HARD_RULES.md`
  - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md`

## 1.3 Phase Read Policy
- 单阶段执行时，只读取当前阶段 checklist 与当前阶段直接需要的文档/模板。
- 多阶段连续执行时，阶段切换后必须：
  - 保留 top-level resident docs
  - 重新读取当前阶段 checklist
  - 丢弃上一阶段的阶段文档、临时 focus、模板填写上下文与局部执行笔记
- 用户若通过问答逐节回填 mother doc，模型回复必须以结构化选项或有界追问为主，不得散讲成长文。
- `Meta-code-graph-base` 不属于 top-level resident docs；它只按阶段承担不同角色。
- 机器侧阶段合同统一从以下工具输出读取：
  - `stage-checklist --stage <stage>`
  - `stage-doc-contract --stage <stage>`
  - `stage-command-contract --stage <stage>`
  - `stage-graph-contract --stage <stage>`

## 2. Stage Order
- `mother_doc`
- `construction_plan`
- `implementation`
- `acceptance`

## 3. Stage Objectives

### `mother_doc`
- 输出目录化 mother doc。
- 明确生产级交付目标、成功定义、关键场景、外部系统、限制、失败语义、验收方式。
- 产出 `requirement_atom` 清单、`baseline_mode` 判断、`blocked_state` 判断、ADR 候选，以及阶段目标/阶段断言/阶段测试/阶段验收。
- 若本项目已有已归档的 `docs/NN_slug` 历史轮次，先抽取上一轮稳定设计、已知 blocker、交付增量和被保留/被替换的决策，再回填当前轮 mother doc。
- mother doc 的回填不是盲开空骨架；它必须结合最近归档迭代历史与当前 code graph/context 一起完成。
- 本阶段的读物边界、命令和 graph 角色以 stage-specific CLI contracts 为准。

### `construction_plan`
- 读取 mother doc 中的设计者规划 `08_dev_execution_plan.md`，并写出独立 `docs/mother_doc/execution_atom_plan_validation_packs/`。
- 这个阶段的目标是“生成 AI 自用的 `Execution_atom_plan&validation_packs`”，显式区别于 mother doc 中的设计规划。
- 若已有图谱，补入现有模块、依赖、影响面、可复用边界。
- 本阶段的读物边界、命令、pack schema 和 graph 角色以 stage-specific CLI contracts、`workflow-contract` 与 `construction-plan-lint` 为准。

### `implementation`
- 严格按当前 active pack 施工。
- 如实现偏离 active pack，先改 `docs/mother_doc/execution_atom_plan_validation_packs/<active_pack>/`，再改代码；若设计意图也改变，再回写 `08_dev_execution_plan.md`。
- 按 `baseline_mode` 选择 clean build 或增量开发路径。
- 默认运行假设是：模型位于可控 WSL/Linux 环境，拥有足够 access 去安装依赖、修复虚拟环境、编辑本地配置、拉起服务并验证本地网络链路。
- `baseline_mode` 只允许依据当前 `HEAD/worktree` 与 runtime 现状判定；git 历史、旧提交、旧 rollout 只能作为参考证据，不能自动触发恢复。
- 若当前 `HEAD/worktree` 近空，且用户没有显式要求恢复旧实现，则默认 `baseline_mode=empty_baseline`。
- 若当前 `HEAD/worktree` 近空，但 README、部署文档或历史提交指向更厚旧实现，这些只能作为背景线索；不得执行 `git show <old_commit>:...`、不得读取旧提交源码/旧测试作为施工素材、不得直接恢复旧提交。
- `needs_baseline_decision` 只用于“当前可见 worktree 自身存在互相冲突的活跃基线信号”，不得因为历史提交更厚而触发。
- 若真实环境缺失，进入 `blocked_state`，暂停伪推进；但这里的“真实环境缺失”仅指外部凭据、第三方账号控制权、远端资源可达性等本地无法自主补齐的条件。
- 施工后执行 graph postflight，为下次维护保留上下文。
- 若已用 commentary 宣布“开始落盘/开始第一批编辑”，下一步必须是实际工具调用或文件编辑；不得长时间停在口头承诺阶段。
- 当前 inner phase 完成后就要执行该 phase 的验证，并把以下内容分域回填到 active pack：
  - `phase_status.jsonl`
  - `evidence_registry.json`
  - `03_validation_and_writeback.md`
  - 必要时回写 `pack_manifest.yaml` 与 `02_inner_dev_phases.md`
- 仅写“功能试过了/命令跑通了”不算合格回填。
- 本阶段的读物边界、graph 禁读规则和退出门命令以 stage-specific CLI contracts 为准。

### `acceptance`
- 在本地可控 WSL 环境内，把所有可本地完成的配置、bring-up、服务常驻、健康检查、模拟人类使用和证据回写做完后，再汇总 requirement-level 验收。
- 交付真实 witness、测试结果、风险与回滚说明。
- 生成按 `requirement_atom` 汇总的 `acceptance_matrix`。
- `acceptance_report` 与 `acceptance_matrix` 固定落在 `docs/mother_doc/acceptance/`，属于当前 mother doc 容器；不得再平铺到 `docs/` 根目录。
- 若 `acceptance-lint` 失败，说明 acceptance 文档领先于实现或证据不真实，必须退回 `construction_plan`/`implementation` 修正。
- 不把 code graph 当验收证据，只把它当解释层。
- `acceptance` 只能基于 mother doc 与前面各阶段已定义的断言/测试/验收做裁决，不得临时补写一套新标准。
- `acceptance` 必须先完成以下本地可解动作，才允许写入 `needs_real_env`：
  - 解析本地 ignored env 文件或项目声明的非 Git config source，补齐 frontend env、runtime endpoint、feature flag、asset base 等配置
  - 把项目声明的本地 ignored config source（本项目默认 `.env.example`）以及相关 env/build/preview 配置真正落到本地 WSL 环境并实测
  - 启动并验证前端运行入口，至少覆盖 dev/build/preview 可用性、路由入口、静态资源和网络连通性
  - 用至少一轮模拟人类使用打通真实链路，并收集日志、浏览器可见行为、网络请求、asset 加载与运行态 witness
- 如果项目把 env 或其他敏感配置明确放在本地 ignored env 文件中，`acceptance` 应直接消费该文件；不得要求这些配置出现在 mother doc 或可推送文档中。
- 如果项目说明或本地 secrets source 已声明大模型目标，`acceptance` 与 bring-up 配置必须写成完整目标表达（例如 `gpt-5.4 reasoning effort high`），不得回退成模糊的 `gpt-5`。
- 本阶段的读物边界、graph 更新动作、收口命令以 stage-specific CLI contracts 为准。

## 4. Requirement Atom Contract
- 每个 `requirement_atom` 至少包含：
  - `requirement_atom_id`
  - `source_clause`
  - `behavior`
  - `non_goals`
  - `failure_semantics`
  - `acceptance_rule`
  - `witness_type`
  - `dependencies`
  - `owner_package_id`

## 5. Baseline Mode Policy
- `baseline_mode` 仅允许以下值：
  - `empty_baseline`
  - `real_codebase`
- 在 `mother_doc` 阶段必须判定一次，在 `implementation` 开始前必须复核一次。
- 当前 `HEAD/worktree` 缺少实质代码且用户未显式要求恢复旧实现时，默认应判定为 `empty_baseline`。
- 判定证据只允许来自：
  - 当前 `HEAD/worktree`
  - 当前 runtime 文档与产物
  - 当前 repo 真实可见文件树
- git 历史、旧提交、旧 session rollout 只能当引用证据，不得单独决定 `baseline_mode`。
- 在 `empty_baseline` 或 `needs_baseline_decision` 下，禁止读取旧提交源码、旧提交测试或历史 rollout 内容作为实现来源。

## 6. Blocked State Policy
- `blocked_state` 仅允许以下值：
  - `clear_to_proceed`
  - `needs_input`
  - `needs_real_env`
  - `needs_baseline_decision`
- 出现 `needs_real_env` 时，不得以 stub、mock、in-memory authority source、自写 witness 继续宣称完成。
- 出现 `needs_real_env` 前，必须先穷尽以下本地可解动作：
  - 安装或修复缺失依赖
  - 修复 `.venv-wsl`、启动命令、PATH、权限位
  - 创建或修正项目声明的本地 ignored secrets source（本项目默认 `.env.example`）以及相关 config/unit 文件
  - 验证前端运行入口、构建结果、预览或部署态、路由、资源加载、以及必要网络连通性
  - 验证真实前端 runtime entry 可执行
  - 使用真实或项目声明的本地 config source 补齐 env/runtime endpoint/feature flags，并进行至少一轮模拟人类使用
- 若以上动作仍未全部尝试，则 `blocked_state` 不能写成 `needs_real_env`。

## 7. Graph Preflight Policy
- graph preflight 的具体调用由 `stage-graph-contract --stage mother_doc|construction_plan` 给出。
- 决策规则仍固定：
  - 已有图谱：读取 `Meta-code-graph-base context/resource`
  - 无图谱但 repo 有实质代码：先运行 `Meta-code-graph-base analyze`
  - 无图谱且 repo 为空或近空：返回 `skip_non_blocking`

## 8. Graph Postflight Policy
- graph postflight 的具体调用由 `stage-graph-contract --stage acceptance` 给出。
- 若 repo 已索引，应建议执行：
  - `detect-changes`
  - `map`
  - `wiki`
- 目标是增强后续 debug、扩展和阅读，不是完成态门禁。

## 9. Required Templates
- 模板索引统一从 `python3 scripts/Cli_Toolbox.py template-index --json` 读取。
- `assets/templates/mother_doc/11_risks_and_blockers.md`
- `assets/templates/execution_atom_plan_validation_packs/00_index.md`
- `assets/templates/execution_atom_plan_validation_packs/PACK_TEMPLATE/*`
- `assets/templates/REQUIREMENT_ATOM_TEMPLATE.md`
- `assets/templates/mother_doc/12_adrs/ADR_TEMPLATE.md`
- `assets/templates/ACCEPTANCE_REPORT_TEMPLATE.md`
- `assets/templates/ACCEPTANCE_MATRIX_TEMPLATE.md`

## 10. Design Phase Plan Required Sections
- `阶段总览`
- `design_step_id`
- `目标 requirement_atoms`
- `前置依赖`
- `实施动作`
- `阶段断言`
- `阶段测试`
- `阶段验收`
- `上线交付 witness`
- `风险与回滚`

## 10.1 Construction Plan Required Sections
- root files：
  - `00_index.md`
  - `pack_registry.yaml`
- per-pack markdown anchors：
  - `00_index.md`
  - `01_scope_and_intent.md`
  - `02_inner_dev_phases.md`
  - `03_validation_and_writeback.md`
- per-pack machine files：
  - `pack_manifest.yaml`
  - `inner_phase_plan.json`
  - `phase_status.jsonl`
  - `evidence_registry.json`
- per-inner-phase fields：
  - `inner_phase_id`
  - `phase_goal`
  - `implementation_slice`
  - `validation_slice`
  - `evidence_writeback_slice`
  - `phase_exit_signal`

## 11. Acceptance Required Fields
- `plan_step_id`
- `implemented_files`
- `tests_run`
- `real_witnesses`
- `residual_risks`
- `rollback_notes`

## 12. Acceptance Matrix Required Fields
- `requirement_atom_id`
- `implemented`
- `tested`
- `witnessed`
- `blocked_state`
- `evidence_refs`

## 13. ADR Required Sections
- `adr_id`
- `title`
- `context`
- `decision`
- `consequences`
- `status`

## 14. Example Commands
```bash
python3 scripts/Cli_Toolbox.py workflow-contract --json
python3 scripts/Cli_Toolbox.py stage-checklist --stage construction_plan --json
python3 scripts/Cli_Toolbox.py stage-doc-contract --stage construction_plan --json
python3 scripts/Cli_Toolbox.py stage-command-contract --stage construction_plan --json
python3 scripts/Cli_Toolbox.py stage-graph-contract --stage construction_plan --json
python3 scripts/Cli_Toolbox.py template-index --json
```
