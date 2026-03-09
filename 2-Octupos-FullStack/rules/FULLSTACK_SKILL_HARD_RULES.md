# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
2. 唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
3. 唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
4. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
5. 本技能显式分为三个阶段：`mother_doc`、`implementation`、`evidence`。
6. 任意阶段开始前，必须先加载顶层规则，不得丢弃：
- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
7. 阶段顺序固定为：`mother_doc -> implementation -> evidence`。
8. `implementation` 阶段必须显式引用 `mother_doc` 阶段产物。
9. `evidence` 阶段必须显式引用 `mother_doc` 与 `implementation` 阶段产物。
10. 整个技能必须采用“抽象层 + 三阶段显式拆分”的写法，禁止任何混写。
11. 抽象功能可共享，特定域命令禁止共享、禁止串用。
12. 文档直接驱动实现；文档骨架直接匹配代码与部署边界。
13. 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合，不是封闭白名单。
14. `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
15. `Mother_Doc/` 当前入口形态应以同名容器目录为主，不保留 `01-07` 这类编号治理目录作为主要结构。
16. `Mother_Doc/README.md` 只承担镜像根说明；`Mother_Doc/agents.md` 才是镜像根递归索引入口。
17. `Mother_Doc` 本身是特例：工作目录容器为 `Octopus_OS/Mother_Doc/`，其自描述文档目录为 `Octopus_OS/Mother_Doc/Mother_Doc/`。
18. `Octopus_OS/Mother_Doc/Mother_Doc/README.md` 说明 `Mother_Doc` 容器自身用途；`Octopus_OS/Mother_Doc/Mother_Doc/agents.md` 是其自描述索引入口。
19. `Mother_Doc` 每一层目录都必须同时具备 `README.md` 与 `agents.md`。
20. `agents.md` 是当前层固定索引文件，必须指向对等层 `README.md` 并列出下一层路径与简短说明。
21. `README.md` 只说明当前层用途、边界与阅读入口，不承载下一层索引枚举。
22. `mother_doc` 阶段每次撰写前，必须先结合上下文使用 `Meta-prompt-write` 强化用户意图。
23. 强化完成后，必须先从 `Mother_Doc/README.md` 与 `Mother_Doc/agents.md` 进入，再逐层读取当前层 `README.md + agents.md`，递归选择直到覆盖完整影响面。
24. 在 `Mother_Doc` 的撰写/维护入口，AI 必须依据用户描述判断是否横向新增容器目录。
25. 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
26. 每个容器文档目录必须先固定为 `README.md + common/`。
27. `common/` 只承载稳定抽象层，不承载 feature-specific 细节。
28. `common/` 当前固定 5 个一级域：`architecture/`、`stack/`、`naming/`、`contracts/`、`operations/`。
29. 每个最小知识点必须单独落一个 `*.md` 文件，不得留空文件。
30. 容器族模板当前固定 5 类：`Mother_Doc`、`UI`、`Gateway`、`Service`、`Data_Infra`。
31. 新增容器后，必须同步生成其容器族对应的 `common/` 抽象层骨架，并刷新相关 `agents.md`。
32. `mother_doc` 回填采用覆盖写入，只维护当前状态；项目内部不规划文档版本，版本控制仅由部署统一承载。
