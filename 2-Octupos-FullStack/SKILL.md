---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责维护 Mother_Doc、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- 本技能采用文档直达实现模型；文档骨架直接匹配代码与部署边界，因此不保留独立的中间 `plan` / `construction_plan` 环节。
- 本技能唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
- 本技能唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
- 容器与目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合，不是封闭白名单。

## 2. 门面边界
- `SKILL.md` 门面只描述本技能如何工作，也就是本技能的自有规则：如何使用本技能、如何撰写 `Mother_Doc`、如何落代码、如何回填 evidence。
- 实际对 UI、event、backend、database、deployment、operations 与运行时细节的设计，不属于本技能自有规则；它们属于本技能产出的被撰写规则，必须落入 `Mother_Doc/`。
- `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
- 运行时消费者必须通过 `Mother_Doc` 容器定义的文档访问 API 获取内容，不以直接文件访问作为消费模型。

## 3. Mother_Doc 入口规则
- `Mother_Doc/` 当前入口形态以同名容器目录为主，不保留 `01-07` 这类编号治理目录。
- `Mother_Doc/README.md` 是镜像根说明，不再承担容器自身索引。
- `Mother_Doc/Mother_Doc/` 是 `Octopus_OS/Mother_Doc/` 容器的自描述目录。
- `Mother_Doc/Mother_Doc/00_INDEX.md` 是 `Mother_Doc` 容器自己的索引入口。
- `Octopus_OS/<Container_Name>/` 与 `Octopus_OS/Mother_Doc/<Container_Name>/` 必须保持同名，供人类、UI 与 AI 直接对号。

## 4. 动态扩容规则
- 在 `Mother_Doc` 的撰写/维护入口，AI 必须依据用户描述判断是否横向新增容器目录，而不是只套用静态参考清单。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增：
  - `Octopus_OS/<Container_Name>/`
  - `Octopus_OS/Mother_Doc/<Container_Name>/`
- `Mother_Doc` 本身是特例：
  - 工作目录容器为 `Octopus_OS/Mother_Doc/`
  - 其自描述文档目录为 `Octopus_OS/Mother_Doc/Mother_Doc/`
- 若用户描述出现新的独立模块，例如 `Mongo_DB`，AI 必须判定是否横向新增对应容器与同名文档目录。

## 5. 抽象层协议
- 每个容器文档目录必须先固定为：`README.md + common/`。
- `common/` 只承载稳定抽象层；业务或功能细节未来再进入 `domains/`、`features/`、`flows/` 等层。
- `common/` 当前固定 5 个一级域：
  - `architecture/`
  - `stack/`
  - `naming/`
  - `contracts/`
  - `operations/`
- 每个最小知识点单独一个 `*.md`，不写空文件。
- 容器族模板当前固定 5 类：
  - `Mother_Doc`
  - `UI`
  - `Gateway`
  - `Service`
  - `Data_Infra`

## 6. 命名约束
- 第一阶段命名规范采用“一个目录 = 一个可独立部署或独立演进的单元”。
- 第一阶段优先使用可读后缀：
  - `_UI`
  - `_Gateway`
  - `_Service`
  - `_DB`
  - `_Cache`
  - `_Broker`
  - `_Storage`
- 第一阶段避免使用会遮蔽边界的大桶名称，例如：
  - `Shared_*`
  - `Business_*`
  - `Runtime_*`

## 7. 规则落点
- 写进技能：
  - 本技能如何被使用
  - `Mother_Doc` 如何被撰写和维护
  - 容器是否需要横向扩充的判定规则
  - 抽象层协议与容器族模板
  - 代码落盘和 evidence 回填规范
  - 技能自有规则与被撰写规则的分层边界
- 写进 `Mother_Doc`：
  - `Mother_Doc` 容器自身的开发文档
  - 各个 UI / gateway / service / data 容器的架构、技术栈、命名、合同与运维规则
  - 具体实现设计、运行边界与部署细节

## 8. 内联导航索引
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [Mother_Doc 入口规则] -> [references/mother_doc/MOTHER_DOC_ENTRY_RULES.md]
- [第一阶段命名参考] -> [references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md]
- [唯一工作目录] -> [/home/jasontan656/AI_Projects/Octopus_OS]
- [唯一文档目录] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc]
- [Mother_Doc 容器索引] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/Mother_Doc/00_INDEX.md]

## 9. 第一阶段工具
- `Cli_Toolbox.materialize_container_layout`
  - 用途：依据 AI 已判定的容器名，生成 `Octopus_OS/<Container_Name>/` 与 `Octopus_OS/Mother_Doc/<Container_Name>/` 的同名目录结构，并补齐容器族对应的 `common/` 抽象层骨架。
  - 边界：工具负责落结构，不负责替 AI 做项目语义判断。
