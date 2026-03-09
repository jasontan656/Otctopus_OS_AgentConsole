# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
2. 唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
3. `Mother_Doc` 容器根固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
4. 唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs/`。
5. `OS_graph` 资产根固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/`。
6. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
7. 本技能显式分为三个阶段：`mother_doc`、`implementation`、`evidence`。
8. 任意阶段开始前，必须先加载顶层常驻文档，不得丢弃：
- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/skill_native/00_SKILL_NATIVE_INDEX.md`
- `references/authored_domains/00_DOMAIN_INDEX.md`
- `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`
9. 进入任一阶段前，必须先读取：
- `stage-checklist --stage <stage>`
- `stage-doc-contract --stage <stage>`
- `stage-command-contract --stage <stage>`
- `stage-graph-contract --stage <stage>`
10. 阶段顺序固定为：`mother_doc -> implementation -> evidence`。
11. 阶段切换时，必须显式丢弃上一阶段的阶段文档与临时 focus，只保留顶层常驻文档。
12. 整个技能必须采用“抽象层 + 三阶段显式拆分”的写法，禁止任何混写。
13. 整个技能必须显式区分：
- `skill_native_rules`
- `authored_domain_rules`
- `container_common_docs`
14. 抽象功能可共享，特定域命令禁止共享、禁止串用。
15. 文档即代码，代码组织最终应与 `Mother_Doc/docs` 组织对齐。
16. `Mother_Doc/docs/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
17. `AGENTS.md` 只允许存在于 `Octopus_OS/Mother_Doc/docs/**`。
18. 实际工作目录容器 `Octopus_OS/<Container_Name>/` 与 `Octopus_OS/Mother_Doc/` 容器根都不得创建 `AGENTS.md`。
19. `Mother_Doc/docs` 每一层目录都必须同时具备：
- `README.md`
- `AGENTS.md`
- `<folder_name>.md`
20. `AGENTS.md` 之外的 `Mother_Doc/docs` markdown 必须带有 `Document Status + Block Registry`。
21. 每次 `mother_doc` 更新非 `AGENTS.md` 文档后，必须把文档级与区块级状态同步标记为：
- `lifecycle_state: modified`
- `requires_development: true`
- `sync_status: modified`
22. 文档如未细分多个区块，默认必须至少存在一个 `block_id: primary`。
23. `README.md` 只承担当前层用途说明。
24. `AGENTS.md` 只承担当前层递归索引。
25. `<folder_name>.md` 只承担当前目录自身这个模块、父级域、黑盒容器或文档承载体的实体说明。
26. `mother_doc` 阶段每次撰写前，必须先结合上下文使用 `Meta-prompt-write` 强化用户意图。
27. 强化完成后，必须先读取 `references/mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md`，判定当前任务属于 `direct_writeback`、`question_backfill` 还是 `AGENTS manager`。
28. `direct_writeback` 只负责把用户已明确描述的内容写入受影响的 `overview / features / shared / common`。
29. `question_backfill` 只负责把未收口问题整理、追问并回填到原文档，不得代替 implementation。
30. `AGENTS manager` 是 `mother_doc` 阶段内的独立子分支，只管理 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`。
31. `AGENTS manager` 固定采用 `scan / collect / push` 三阶段；不得与普通文档正文覆盖写回混写。
32. 完成子分支判定后，必须从 `Octopus_OS/Mother_Doc/docs/` 根层 `README.md + AGENTS.md + Mother_Doc.md` 进入，再逐层读取当前层 `README.md + AGENTS.md + <folder_name>.md`，递归覆盖完整影响面。
33. `mother_doc` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕；本阶段只负责覆盖式更新当前文档状态。
33.1 `mother_doc` 结束前必须运行本地 `git` 驱动的状态脚本；变更文档写成 `modified`，空占位写成 `null`，清洁但已闭环的文档保持 `developed`。
34. 产物域规则必须分域承载，不得把 UI、Gateway、Service、Data_Infra 全部收敛为统一的 `mother_doc` 文档规则。
35. 各产物域至少固定包含：
- 一套 `writing_guides`
- 一套 `code_abstractions`
- 一套 `dev_canon`
36. 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合，不是封闭白名单。
37. 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc/docs` 同名目录。
38. 每个容器文档目录必须先固定为 `README.md + AGENTS.md + <folder_name>.md + overview/ + features/ + shared/ + common/`。
39. `overview/` 承载人类可观测总览层。
40. `features/` 承载功能层，单个文档可以覆盖单文件或多文件的语义等价单元。
41. `shared/` 承载 API、event、共享合同、跨容器依赖和对应未收口问题。
42. `common/` 只承载稳定抽象层，不承载 feature-specific 细节。
43. `common/` 至少固定 3 个一级域：`writing_guides/`、`code_abstractions/`、`dev_canon/`。
44. `common/code_abstractions/` 下至少固定 5 个二级域：`architecture/`、`stack/`、`naming/`、`contracts/`、`operations/`。
45. `Mother_Doc` 容器自己的 `common/` 额外固定包含 `development_logs/`。
46. 每个最小知识点必须单独落一个 `*.md` 文件，不得留空文件。
47. 容器族模板当前固定 5 类：`Mother_Doc`、`UI`、`Gateway`、`Service`、`Data_Infra`。
48. `implementation` 阶段必须像独立人类开发者一样推进：自行安装依赖、修复环境、运行测试、bring-up、验证、回填。
49. `implementation` 阶段发现 `Mother_Doc/docs` 与代码库/运行时不一致时，必须显式更新代码、文档或两者以恢复一致，不得忽略 drift。
50. `implementation` 进入具体容器前，必须先读取对应域族的 `implementation` 规则与 `dev_canon`，然后再读取该容器自己的 `common/code_abstractions` 与其他文档层。
51. `implementation` 规则属于技能运行规则与域族规则，不得下沉到 `Mother_Doc` 产物模板中。
52. `implementation` 只负责差异识别、代码施工与对齐回写；本阶段消费 `modified` 状态，但不得把状态提前改成 `developed`。
53. `implementation` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕；这些留痕只能在 `evidence` 或 `implementation -> evidence` 联动中完成。
54. 首次无代码时，implementation 仍必须按“先读代码、再读更新后文档”的比较顺序施工；空代码基线也是有效比较对象。
55. 只有在本地可控范围内的依赖修复、环境修复、配置补齐、服务拉起、测试执行都已穷尽后，才允许进入真实 blocked 状态。
56. `evidence` 阶段的 graph 主体是 `OS_graph`，它同时管理文档 graph、代码 graph、模块映射、日志节点与 evidence 绑定。
57. `OS_graph` 固定拆成 `narrative_layer`、`contract_layer`、`implementation_layer`、`evidence_layer` 四层。
58. evidence 必须是真实 witness，不得伪造，不得把 `OS_graph` 降级成只解释代码的附属图。
59. implementation batch 与 deployment checkpoint 都只能在 `evidence` 阶段追加到 `Octopus_OS/Mother_Doc/docs/Mother_Doc/common/development_logs/`。
60. `evidence` 阶段独占 Git / GitHub 留痕；开发/部署日志只保留摘要，该摘要必须等于同轮 Git 提交 message，具体文件与代码改动由 Git / GitHub 承担追踪。
60.1 `evidence` 在 graph、日志和 witness 闭环完成后，必须把对应文档/区块状态回写为 `developed`。
61. `mother_doc`、`implementation`、`evidence` 的回填都采用覆盖写入，只维护当前状态；项目内部不规划文档版本，但开发/部署日志承担时间线与检查点语义。
