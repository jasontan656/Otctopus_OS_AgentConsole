# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
2. 唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
3. 唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
4. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
5. 本技能显式分为三个阶段：`mother_doc`、`implementation`、`evidence`。
6. 任意阶段开始前，必须先加载顶层常驻文档，不得丢弃：
- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`
7. 进入任一阶段前，必须先读取：
- `stage-checklist --stage <stage>`
- `stage-doc-contract --stage <stage>`
- `stage-command-contract --stage <stage>`
- `stage-graph-contract --stage <stage>`
8. 阶段顺序固定为：`mother_doc -> implementation -> evidence`。
9. 阶段切换时，必须显式丢弃上一阶段的阶段文档与临时 focus，只保留顶层常驻文档。
10. 整个技能必须采用“抽象层 + 三阶段显式拆分”的写法，禁止任何混写。
11. 抽象功能可共享，特定域命令禁止共享、禁止串用。
12. 文档即代码，代码组织最终应与 `Mother_Doc` 组织对齐。
13. `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
14. `agents.md` 只允许存在于 `Octopus_OS/Mother_Doc/**`。
15. 实际工作目录容器 `Octopus_OS/<Container_Name>/` 不得创建 `agents.md`。
16. `Mother_Doc` 每一层目录都必须同时具备：
- `README.md`
- `agents.md`
- `<folder_name>.md`
17. `agents.md` 之外的 `Mother_Doc` markdown 必须带有 `Document Status + Block Registry`。
18. 每次 `mother_doc` 更新非 `agents.md` 文档后，必须把文档级与区块级状态同步标记为：
- `requires_development: true`
- `sync_status: pending_implementation`
19. 文档如未细分多个区块，默认必须至少存在一个 `block_id: primary`。
20. `README.md` 只承担当前层用途说明。
21. `agents.md` 只承担当前层递归索引。
22. `<folder_name>.md` 只承担当前目录自身这个模块、父级域、黑盒容器或文档承载体的实体说明。
23. `mother_doc` 阶段每次撰写前，必须先结合上下文使用 `Meta-prompt-write` 强化用户意图。
24. 强化完成后，必须先从根层 `README.md + agents.md + Mother_Doc.md` 进入，再逐层读取当前层 `README.md + agents.md + <folder_name>.md`，递归覆盖完整影响面。
25. 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合，不是封闭白名单。
26. 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
27. 每个容器文档目录必须先固定为 `README.md + agents.md + <folder_name>.md + common/`。
28. `common/` 只承载稳定抽象层，不承载 feature-specific 细节。
29. `common/` 至少固定 5 个一级域：`architecture/`、`stack/`、`naming/`、`contracts/`、`operations/`。
30. `Mother_Doc` 容器自己的 `common/` 额外固定包含 `development_logs/`。
31. 每个最小知识点必须单独落一个 `*.md` 文件，不得留空文件。
32. 容器族模板当前固定 5 类：`Mother_Doc`、`UI`、`Gateway`、`Service`、`Data_Infra`。
33. `implementation` 阶段必须像独立人类开发者一样推进：自行安装依赖、修复环境、运行测试、bring-up、验证、回填。
34. `implementation` 阶段发现 `Mother_Doc` 与代码库/运行时不一致时，必须显式更新代码、文档或两者以恢复一致，不得忽略 drift。
35. 实现完成后，必须把对应文档/区块状态从 `pending_implementation` 回写为 `aligned`，并追加 implementation batch 日志。
36. `implementation` 的日志固定追加到 `Octopus_OS/Mother_Doc/Mother_Doc/common/development_logs/implementation_batches.md`。
37. 首次无代码时，implementation 仍必须写首条 batch 日志，把当前文档状态视为领先于空代码基线的实现输入。
38. 只有在本地可控范围内的依赖修复、环境修复、配置补齐、服务拉起、测试执行都已穷尽后，才允许进入真实 blocked 状态。
39. `evidence` 阶段的 graph 主体是 `OS_graph`，它同时管理文档 graph、代码 graph、模块映射、日志节点与 evidence 绑定。
40. evidence 必须是真实 witness，不得伪造，不得把 `OS_graph` 降级成只解释代码的附属图。
41. deployment checkpoint 只能在存在真实部署/上线 witness 时追加到 `Octopus_OS/Mother_Doc/Mother_Doc/common/development_logs/deployment_batches.md`。
42. `mother_doc`、`implementation`、`evidence` 的回填都采用覆盖写入，只维护当前状态；项目内部不规划文档版本，但开发/部署日志承担时间线与检查点语义。
