# OCTOPUS Skill Hard Rules

适用技能：
- `4-Octupos-OS-Frontend`

## Rule Set

1. 本技能输出的文档必须优先保证人类可读性，不得退化成 machine-first 工件集合。
2. `mother_doc` 是唯一需求源；code graph 只能补充现状与结构边界，不得替代需求源。
3. 顶层阶段固定为：
- `mother_doc`
- `construction_plan`
- `implementation`
- `acceptance`
4. 顶层常驻文档固定为：
- `rules/OCTOPUS_SKILL_HARD_RULES.md`
- `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`
- `/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend/AGENTS.md`
5. 每个阶段只能做本阶段的事，禁止跨阶段混写；进入新阶段前必须先读取 `stage-checklist --stage <current_stage>`。
6. 阶段切换时只允许保留顶层常驻文档；上一阶段的 checklist、阶段文档、临时 focus、模板填写上下文必须显式丢弃，除非当前阶段合同明确要求重新读取。
7. `mother_doc` 阶段必须先把需求固化成目录化项目说明与 `requirement_atom`；没有完整说明书，不得进入 `construction_plan`。
7.0 `mother_doc` 阶段文档只允许包含：`docs/mother_doc/*` 与 `assets/templates/mother_doc/*`；不得提前读取 construction packs、implementation 证据或 acceptance artifacts。
7.0.1 若 `docs/` 下已经存在编号归档的 `NN_slug` 目录，`mother_doc` 阶段必须先读取最新一轮归档，并抽取仍然有效的目标、架构决策、blocker 与交付增量；不得把新 mother_doc 当成与历史脱钩的空白起点。
7.1 `mother_doc` 在进入 `construction_plan` 前必须通过 `mother-doc-lint`；若结构缺失、仍有 `replace_me`、缺少阶段断言/阶段测试/阶段验收，或出现 `最小闭环`、`最小实现`、`mvp`、`test profile` 等降级语义，必须先修正文档。
7.2 发现范围固定限制为：`Octopus_CodeBase_Backend`、`OctuposOS_Runtime_Backend`、固定 `docs/` 与 `docs/mother_doc/` 路径，以及必要 skill 文件。
7.3 若启动 cwd 恰好是 `/home/jasontan656/AI_Projects`，它只是容器根/钩子根，不得被视为 discoverable repo。
7.4 禁止为了找上下文扫描整个 `/home/jasontan656/AI_Projects`，也不得读取 `Human_Work_Zone`、`GoogleDriveDump` 等 sibling 区域，除非 mother doc 显式引用。
7.5 极简 prompt 启动时，第一批动作必须固定为：直接读取固定 `docs/mother_doc/00_index.md` 或执行 `mother-doc-init` 创建骨架；若已存在编号归档的 `docs/NN_slug`，先读取最新一轮归档；运行 `mother-doc-lint`；在 `mother_doc` 阶段若已有图谱必须读取它来校准现有代码现实；不得先用 `rg/find/ls` 在 workspace 根定位需求或仓库。
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
10.1 ADR 运行产物固定收敛在当前 `docs/mother_doc/12_adrs/`；不得再平铺第二套 `docs/adr` 根目录。
11. `08_dev_execution_plan.md` 只表示 mother doc 内的设计者规划；它必须至少写清：
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
13. `construction_plan` 阶段必须单独产出 `docs/mother_doc/execution_atom_plan_validation_packs/`；术语使用 `Execution_atom_plan&validation_packs`，文件系统 slug 固定为 `execution_atom_plan_validation_packs`。
14. construction packs 的 root/file schema、numbered packs、machine files 与 inner phase 结构必须满足 `construction-plan-lint` 与 `workflow-contract`；不得自造平替布局。
17. `implementation` 阶段的读物边界、禁读 graph 规则与阶段切换丢弃项以 `stage-doc-contract --stage implementation` 与 `stage-graph-contract --stage implementation` 为准；不得把未激活 pack 或 acceptance 判决文档带进实现 focus。
18. 模型不得跳过 `docs/mother_doc/execution_atom_plan_validation_packs/` 直接靠代码和测试定义真实意图。
19. 若 implementation 与 active pack 发生偏离，必须先回写当前 pack 的 machine files 与 markdown anchors；若设计意图也变化，再回写 `08_dev_execution_plan.md`。
20. implementation 回填的测试结果必须说明“为什么这组测试证明了设计理念与失败语义”，而不是只记录“功能试过了”。
21. `acceptance` 阶段的读物边界、graph 更新动作与收口命令以 `stage-doc-contract --stage acceptance`、`stage-command-contract --stage acceptance`、`stage-graph-contract --stage acceptance` 为准；不得把 graph 当验收证据，也不得保留 implementation 局部调试 focus 来替代交付裁决。
22. 验收必须绑定真实行为与真实 witness，不接受只靠自写 report、自写状态字段宣称完成。
22.1 `acceptance` 不只是写报告；它必须把本地可控环境真正配到可运行状态，包括 token/webhook secret/owner allowlist/runtime endpoint、常驻服务、healthz/connectivity、以及至少一轮模拟人类使用。
22.2 若项目已声明本地 ignored env 文件或其他非 Git secrets source，`acceptance` 必须直接使用它们，不得要求这些 secrets 回写进 mother doc、runtime 文档或任何可推送文件。
22.3 在本地可控 bring-up 尚未完成前，不得把 `needs_real_env` 当作收尾出口。
22.4 若项目已声明模型目标，必须使用完整模型目标表达（例如 `gpt-5.4 reasoning effort high`），不得写成模糊的 `gpt-5` 或其他会丢失精度的缩写。
23. 最终验收必须产出 `acceptance_matrix`，并按 `requirement_atom` 逐条给出 `implemented/tested/witnessed/blocked_state`。
23.0 `acceptance_report` 与 `acceptance_matrix` 运行产物固定收敛在当前 `docs/mother_doc/acceptance/`；不得把这两份文档平铺到 `docs/` 根目录。
23.1 `acceptance_matrix` 与 `acceptance_report` 中的 `implemented=true`、`tested=true` 只能引用当前磁盘上已经存在的实现/测试证据；不得把“计划要写的文件”提前写成成功态。
23.2 在 acceptance 收口前必须通过 `acceptance-lint`；若 lint 报出 evidence path 不存在、`needs_real_env` 下错误写 `witnessed=true`、或 acceptance 早于 implementation，则必须回退修正。
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
