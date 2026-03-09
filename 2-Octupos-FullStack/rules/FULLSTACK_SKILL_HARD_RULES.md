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
9. 实际对 UI 的设计、event 设计、后端支持、数据库边界、部署拓扑与其他实现细节，必须落入被撰写规则中，不得堆回 `SKILL.md` 门面。
10. `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
11. `Mother_Doc/` 文件在仓库内作为源文档存在，但运行时消费者必须通过 `Mother_Doc_Service` API 获取内容，不以直接文件访问作为消费模型。
12. `Mother_Doc/` 当前入口形态应以同名容器目录为主，不保留 `01-07` 这类编号治理目录作为主要结构。
13. 在 `Mother_Doc` 的撰写/维护入口，AI 必须依据用户描述判断是否横向新增容器目录。
14. 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
15. `Mother_Doc` 本身是特例：工作目录容器为 `Octopus_OS/Mother_Doc/`，其自描述文档目录为 `Octopus_OS/Mother_Doc/Mother_Doc/`。
16. 第一阶段命名规范采用“一个目录 = 一个可独立部署或独立演进的单元”。
17. 第一阶段优先使用 `_UI`、`_Gateway`、`_Service`、`_DB`、`_Cache`、`_Broker`、`_Storage` 等后缀。
18. 第一阶段避免使用 `Shared_*`、`Business_*`、`Runtime_*` 这类会遮蔽边界的大桶名称。
19. 技能写文档是一回事；按照文档开发出来的内容是另一回事，二者边界必须清楚。
