---
doc_id: workflow_centralflow2_octppusos.rules_octopus_skill_hard_rules
doc_type: topic_atom
topic: OCTOPUS Skill Hard Rules
anchors:
- target: ../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# OCTOPUS Skill Hard Rules

## 迁移说明
- 本文件当前作为迁移期支撑规则保留。
- 新的主链真源位于 `path/development_loop/` 与其 `steps/` 子树。

适用技能：
- `Workflow-CentralFlow2-OctppusOS`

## Rule Set

1. 本技能输出的文档必须优先保证人类可读性，不得退化成 machine-first 工件集合。
2. `mother_doc` 是唯一需求源；code graph 只能补充现状与结构边界，不得替代需求源。
3. 顶层阶段固定为：
- `mother_doc`
- `construction_plan`
- `implementation`
- `acceptance`
4. 顶层常驻文档固定为：
- `path/development_loop/10_CONTRACT.md`
- `path/development_loop/15_TOOLS.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`
- `<docs_root>/AGENTS.md`（若存在）
- `/home/jasontan656/.codex/skills/Dev-ProjectStructure-Constitution/SKILL.md`（当 `docs_root` 尚未固定时）
5. 每个阶段只能做本阶段的事，禁止跨阶段混写；进入新阶段前必须先读取 `stage-checklist --stage <current_stage>`。
5.1 在进入任一阶段前，必须先运行 `target-runtime-contract`，确认当前 `target_root` 是 `AI_Projects` 内当前代码对象的 repo root 边界，并以 `docs_root / mother_doc_root / execution_atom_plan_validation_packs / graph_runtime_root` 解析实际工作目标。
5.2 当前代码对象自己的 `docs_root` 必须先存在；不存在时，本技能必须拒绝服务，不得私自创建主题容器。
5.2.0 仅完成项目结构初始化时，`Development_Docs/` 本身允许为空；但一旦进入本技能的开发闭环，`docs_root` 必须已经是当前代码对象真实存在的开发文档根，而不是再重复下一层对象目录。
5.2.1 `target_root` 还必须位于 `AI_Projects` workspace 内；否则 `$Meta-RootFile-Manager` 无法收治模块 `AGENTS.md`，本技能必须拒绝服务。
5.3 若目标项目已经固定开发文档容器，必须按 `Dev-ProjectStructure-Constitution` 的判定使用该容器；不得自行改投到另一个 `docs/` 或 sibling 目录。
5.4 若目标模块文件夹中已经存在 `execution_atom_plan_validation_packs/`、`pack_registry.yaml`、编号归档 `NN_slug` 或既有 graph，必须先判定它们的生命周期与合法性；不得把 `preview_skeleton` 或 `accepted/retired` 的旧 official plan 当成当前轮 construction input 复用，也不得为同一目标另外创建脱节的母文档、pack 树或图谱脉络。
5.5 目标模块的 `AGENTS.md` 必须使用本技能模版创建，并在创建后立即通过 `$Meta-RootFile-Manager collect` 收治；不得在未受管状态下长期存在。
6. 阶段切换时只允许保留顶层常驻文档；上一阶段的 checklist、阶段文档、临时 focus、模板填写上下文必须显式丢弃，除非当前阶段合同明确要求重新读取。
7. `mother_doc` 阶段必须先把需求固化成目录化项目说明与 `requirement_atom`；没有完整说明书，不得进入 `construction_plan`。
7.0 `mother_doc` 必须采用协议驱动原子文档树；固定根入口只保留 `00_index.md`，其余文档允许按设计思路自由新增、插入、迁移与重排，但不得回退成 giant mother_doc 单文件。
7.0.1 `00_index.md` 不得手工维护文件清单；必须通过 `mother-doc-refresh-root-index` 自动从当前 folder 结构生成，只展示目录级结构图，不展示文件。
7.0.0 每个 mother_doc 原子文档都必须带 frontmatter：`doc_work_state`、`doc_pack_refs`、`thumb_title`、`thumb_summary`、`display_layer`、`always_read`、`anchors_down`、`anchors_support`；合法状态只有 `modified -> planned -> developed -> ref`。
7.0.0.1 `display_layer` 只表示页面从上到下的显示分层；它不参与树遍历，只负责显示分层。
7.0.0.2 `anchors_down` 是“主链子节点集合”；列表顺序就是主链兄弟顺序，viewer 必须按列表顺序递归向下爬。
7.0.0.3 `anchors_support` 是“支撑子树入口集合”；列表顺序就是 support 兄弟顺序，viewer 必须把它们当成从当前节点长出的旁支树继续递归。
7.0.0.4 `anchors_down` 与 `anchors_support` 的值必须统一写成相对 `mother_doc` 根的文档路径；不得混入 `doc_id`、标题或其他推断值。
7.0.0.5 同一个子文档只能有一个父节点；一旦同一目标同时出现在多个父节点的 `anchors_down/anchors_support` 里，lint 必须判失败。
7.0.0.6 `anchors_down` 的目标必须落到更深的 `display_layer`；`anchors_support` 的目标必须落到同层或更深的 `display_layer`。
7.0.0.7 兄弟节点默认不互连；layer 兄弟不互连，container 兄弟不互连，viewer 只能把它们显示成同父集合。
7.0.0.8 `anchors_up/right/left` 不再属于合法 mother_doc 协议字段；viewer 与 workflow 均不得继续依赖这三个方向。
7.0.0.3 只要某一轮 mother_doc 实际新增了本技能尚未声明的协议规则，该轮就必须同步回写 `$Workflow-CentralFlow2-OctppusOS` 的 mother_doc 合同、lint 与模板。
7.0 `mother_doc` 阶段文档只允许包含：`<docs_root>/mother_doc/*` 与 `path/development_loop/steps/mother_doc/templates/mother_doc/*`；不得提前读取 construction packs、implementation 证据或 acceptance artifacts。
7.0.1 若当前模块文档根下已经存在编号归档的 `NN_slug` 目录，`mother_doc` 阶段必须先读取最新一轮归档，并抽取仍然有效的目标、架构决策、blocker 与交付增量；不得把新 mother_doc 当成与历史脱钩的空白起点。
7.1 `mother_doc` 在进入 `construction_plan` 前必须通过 `mother-doc-lint`；若结构缺失、仍有 `replace_me`、缺少阶段断言/阶段测试/阶段验收，或出现 `最小闭环`、`最小实现`、`mvp`、`test profile` 等降级语义，必须先修正文档。
7.2 发现范围固定限制为：当前 `target_root` 边界、已判定的 `docs_root`、`mother_doc/`、当前 `codebase_root`、必要 skill 文件与必要 graph 文件。
7.3 若启动 cwd 恰好是 `/home/jasontan656/AI_Projects`，它只是容器根/钩子根，不得被视为 discoverable repo。
7.4 禁止为了找上下文扫描整个 `/home/jasontan656/AI_Projects`，也不得读取 `Human_Work_Zone`、`GoogleDriveDump` 等 sibling 区域，除非 mother doc 显式引用。
7.5 极简 prompt 启动时，第一批动作必须固定为：先运行 `target-runtime-contract`；必要时读取 `Dev-ProjectStructure-Constitution` 以确认模块文档容器；若模块容器可用但骨架未齐，先运行 `target-scaffold`；再读取当前 `mother_doc/00_index.md`；若已存在编号归档的 `NN_slug`，先读取最新一轮归档；若已存在任务包，先读取并复用当前任务包；当 folder 结构有变化时先运行 `mother-doc-refresh-root-index`；运行 `mother-doc-lint`；在 `mother_doc` 阶段若已有图谱必须读取它来校准现有代码现实；不得先用 `rg/find/ls` 在 workspace 根盲扫需求或仓库。
6. `baseline_mode` 必须显式判定：
- `empty_baseline`
- `real_codebase`
 - 判定只允许依据当前 `HEAD/worktree`、当前 runtime 文档与当前可见文件树。
 - git 历史、旧提交、旧 rollout 只能作参考证据，不得单独把基线抬升成恢复路径。
 - 若当前 `HEAD/worktree` 近空且用户未显式要求恢复旧实现，默认判定为 `empty_baseline`。
 - 若当前 `HEAD/worktree` 近空，但 README、部署文档或历史提交更厚，这些只能作为背景线索；不得执行 `git show <old_commit>:...`、不得读取旧提交源码/旧测试作为施工素材、不得直接恢复旧提交。
 - `needs_baseline_decision` 只用于当前可见 worktree 自身存在互相冲突的活跃基线信号，不得因为历史提交更厚而触发。
7. `blocked_state` 必须显式表达：
- `clear_to_proceed`
- `needs_input`
- `needs_real_env`
- `needs_baseline_decision`
- 若处于非 `clear_to_proceed`，不得伪造继续完成。
7.1 `needs_real_env` 不是“本地不想继续”的出口；进入它之前，必须在 `07_env_and_deploy.md` 与 `11_risks_and_blockers.md` 中写清本地已穷尽动作与仍缺外部条件。
7.2 只有在真正缺少外部凭据、第三方账号控制权、远端服务接入条件，或外部资源客观不可得时，才允许保留 `needs_real_env`。
8. package 数量不得由固定 min/max 规则控制，只能由需求粒度、依赖关系和可读性决定。
9. `package dependency graph` 若需要显式产出，必须调用 `Meta-code-graph-base` 或读取其结果，不得在章鱼技能内部重复造一套。
10. ADR 必须独立记录长期架构决策，不得把稳定架构裁决埋进一次性实现叙事。
10.1 ADR 运行产物固定收敛在当前 `<docs_root>/mother_doc/12_adrs/`；不得再平铺第二套 `adr` 根目录。
11. 若存在 `doc_role=design_plan` 文档，它表示 mother doc 内的设计者规划；它可以作为 construction_plan 的普通输入之一，但不得再成为唯一强依赖入口。该类文档若要承载阶段规划，至少写清：
- 阶段总览
- design_step_id
- 覆盖哪些 requirement atoms
- 依赖与顺序
- 实施动作
- 阶段断言
- 阶段测试
- 阶段验收
- 上线交付 witness
- 风险与回滚
12. `construction_plan` 阶段文档边界、命令与 graph 角色以 `stage-doc-contract --stage construction_plan`、`stage-command-contract --stage construction_plan`、`stage-graph-contract --stage construction_plan` 为准；不得把 implementation 落盘证据或 acceptance 判决文档混进本阶段。
13. `construction_plan` 阶段必须单独产出 `<docs_root>/mother_doc/execution_atom_plan_validation_packs/`；术语使用 `Execution_atom_plan&validation_packs`，文件系统 slug 固定为 `execution_atom_plan_validation_packs`。
13.1 `construction_plan` 不得再强依赖单个 `doc_role=design_plan` 或固定 `08_dev_execution_plan.md`；它必须先爬完整 mother_doc 树，找出 `doc_work_state=modified` 的原子文档，再结合锚点和上下文自行决定 pack 拆分。
14. construction packs 的 root/file schema、numbered packs、machine files 与 inner phase 结构必须满足 `construction-plan-lint` 与 `workflow-contract`；不得自造平替布局。
14.0 `construction_plan` 只能从已通过 `mother-doc-lint` 的 mother doc 正式生成；若只是想看骨架形态，只能生成 `preview_skeleton`，并且它必须显式带 `execution_eligible=false`、`state_sync_eligible=false`、`plan_state=preview_only`。
14.0.1 official plan 与 preview skeleton 必须显式区分；未带 `plan_kind` / `plan_state` 生命周期字段的 pack 树视为非法 construction plan。
14.0.2 official plan 初始状态只能是 `planned_unused`；进入 implementation 后才允许切到 `in_execution`，并且 `accepted/retired` 后不得回到新一轮 construction input。
14.1 任何文档从 `modified` 迁移到 `planned` 前，必须先被至少一个真实 `NN_slug` pack 吸收，并在文档侧记录 `doc_pack_refs`。
14.2 每个 pack 必须显式声明 `source_mother_doc_refs`；implementation 只允许回读这些 source refs，不得通读整个 mother_doc 树。
17. `implementation` 阶段的读物边界、禁读 graph 规则与阶段切换丢弃项以 `stage-doc-contract --stage implementation` 与 `stage-graph-contract --stage implementation` 为准；不得把未激活 pack 或 acceptance 判决文档带进实现 focus。
18. 模型不得跳过 `<docs_root>/mother_doc/execution_atom_plan_validation_packs/` 直接靠代码和测试定义真实意图。
19. 若 implementation 与 active pack 发生偏离，必须先回写当前 pack 的 machine files 与 markdown anchors；若设计意图也变化，再回写对应 `doc_role=design_plan` 文档与受影响的 mother_doc 原子文档。
20. implementation 回填的测试结果必须说明“为什么这组测试证明了设计理念与失败语义”，而不是只记录“功能试过了”。
20.1 implementation 只允许把与当前 active pack 关联的文档从 `planned` 迁移到 `developed`；不得批量推进无关文档状态。
21. `acceptance` 阶段的读物边界、graph 更新动作与收口命令以 `stage-doc-contract --stage acceptance`、`stage-command-contract --stage acceptance`、`stage-graph-contract --stage acceptance` 为准；不得把 graph 当验收证据，也不得保留 implementation 局部调试 focus 来替代交付裁决。
22. 验收必须绑定真实行为与真实 witness，不接受只靠自写 report、自写状态字段宣称完成。
22.1 `acceptance` 不只是写报告；它必须把本地可控环境真正配到可运行状态，包括项目声明的凭据、runtime endpoint、常驻运行面、health/connectivity，以及至少一轮模拟人类或操作员使用。
22.2 若项目已声明本地 ignored env 文件或其他非 Git secrets source，`acceptance` 必须直接使用它们，不得要求这些 secrets 回写进 mother doc、runtime 文档或任何可推送文件。
22.3 在本地可控 bring-up 尚未完成前，不得把 `needs_real_env` 当作收尾出口。
22.4 若项目已声明模型目标、浏览器目标、运行目标或其他关键目标表达，必须使用完整目标表达，不得写成会丢失精度的模糊缩写。
23. 最终验收必须产出 `acceptance_matrix`，并按 `requirement_atom` 逐条给出 `implemented/tested/witnessed/blocked_state`。
23.0 `acceptance_report` 与 `acceptance_matrix` 运行产物固定收敛在当前 `<docs_root>/mother_doc/acceptance/`；不得把这两份文档平铺到模块文档根目录。
23.1 `acceptance_matrix` 与 `acceptance_report` 中的 `implemented=true`、`tested=true` 只能引用当前磁盘上已经存在的实现/测试证据；不得把“计划要写的文件”提前写成成功态。
23.2 在 acceptance 收口前必须通过 `acceptance-lint`；若 lint 报出 evidence path 不存在、`needs_real_env` 下错误写 `witnessed=true`、或 acceptance 早于 implementation，则必须回退修正。
23.3 只有当 acceptance/evidence 完成且 graph postflight 已执行后，相关 mother_doc 文档才允许从 `developed` 迁移到 `ref`。
23.4 当本轮设计或实现真实改动了 mother_doc 时，模型必须先判断应回到 `modified` 的原子文档，再使用 `mother-doc-mark-modified --auto-from-git` 作为 Git diff / impact 兜底检查；不得完全依赖自动扫描替代模型判断。
24. code graph 的阶段角色以 `stage-graph-contract --stage <stage>` 为准；不得在其他文档中另造一套分阶段图谱语义。
25. code graph 不是 blocker 工厂：
- 有图谱时在 `mother_doc` 与 `construction_plan` 阶段必须读取并使用
- 无图谱但 repo 已有实质代码时必须建议更新
- 无图谱且 repo 为空或近空时必须允许继续，不得卡死首次落盘
26. acceptance/evidence 收口后必须回看并更新 code graph：
- 至少判断是否需要 `detect-changes`
- 需要时生成 `map/wiki`
- 目标是为下次 debug 和扩展提供可读导航，不是当前轮 acceptance 证据
27. 文档与模板默认中文叙事；代码、CLI 输出字段、注释使用 English。
28. mother doc 与 execution packs 模板中的填写规范必须随骨架一起创建，并用 Python 注释语义表达；进入下一阶段前，这些规范与所有 `replace_me` 都必须被真实内容替换掉。
29. 一旦模型用 commentary 宣布“开始落盘”“第一批编辑”“现在开始写代码/文档”，下一步必须紧跟真实工具调用或文件编辑；若没有落盘动作就长时间静默，视为 `violation`。
30. 每个阶段都必须写清自己的阶段目标、阶段断言、阶段测试、阶段验收，不得把验证全部挤到最终 `acceptance` 一次性处理。
31. user-facing 合同、门面、模板与测试中不得把本技能描述成“升级版”“从旧流程迁移而来”；只允许保留中性的“单文件输入不受支持”与“仅当前 worktree 可作实现来源”约束。
32. `mother_doc` 的顺序归档只属于 acceptance/evidence 收口动作；implementation 不得提前执行目录改名。
