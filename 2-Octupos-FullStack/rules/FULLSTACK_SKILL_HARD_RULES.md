# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
2. 本技能采用文档直达实现模型；文档骨架直接匹配代码与部署边界，因此不保留独立的中间 `plan` / `construction_plan` 环节。
3. 唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
4. 唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
5. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
6. 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合，不是封闭白名单。
7. 必须显式区分两类规则：
- `技能自有规则`：本技能如何工作、如何写文档、如何落盘、如何回填 evidence
- `被撰写规则`：本技能产出的开发运维文档中，对 UI、event、后端、数据库、部署、运维与运行时对象的规则
8. `SKILL.md` 门面只描述技能自有规则。
9. 实际对 UI、event、backend、database、deployment、operations 与其他实现细节的设计，必须落入被撰写规则中，不得堆回 `SKILL.md` 门面。
10. `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
11. `Mother_Doc/README.md` 只承担镜像根说明；`Mother_Doc/Mother_Doc/00_INDEX.md` 才是 `Mother_Doc` 容器自身的索引入口。
12. `Mother_Doc/` 当前入口形态应以同名容器目录为主，不保留 `01-07` 这类编号治理目录作为主要结构。
13. 在 `Mother_Doc` 的撰写/维护入口，AI 必须依据用户描述判断是否横向新增容器目录。
14. 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
15. `Mother_Doc` 本身是特例：工作目录容器为 `Octopus_OS/Mother_Doc/`，其自描述文档目录为 `Octopus_OS/Mother_Doc/Mother_Doc/`。
16. 每个容器文档目录必须先固定为 `README.md + common/`。
17. `common/` 只承载稳定抽象层，不承载 feature-specific 细节。
18. `common/` 当前固定 5 个一级域：`architecture/`、`stack/`、`naming/`、`contracts/`、`operations/`。
19. 每个最小知识点必须单独落一个 `*.md` 文件，不得留空文件。
20. 容器族模板当前固定 5 类：`Mother_Doc`、`UI`、`Gateway`、`Service`、`Data_Infra`。
21. 新增容器后，必须同步生成其容器族对应的 `common/` 抽象层骨架。
22. 第一阶段命名规范采用“一个目录 = 一个可独立部署或独立演进的单元”。
23. 第一阶段优先使用 `_UI`、`_Gateway`、`_Service`、`_DB`、`_Cache`、`_Broker`、`_Storage` 等后缀。
24. 第一阶段避免使用 `Shared_*`、`Business_*`、`Runtime_*` 这类会遮蔽边界的大桶名称。
25. 技能写文档是一回事；按照文档开发出来的内容是另一回事，二者边界必须清楚。
