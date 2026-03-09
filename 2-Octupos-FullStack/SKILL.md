---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责维护 Mother_Doc、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责维护 `Mother_Doc`、开发代码并回填 evidence。
- 本技能唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
- 本技能唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
- 文档直接驱动实现；容器集合允许按项目描述动态横向扩充。

## 2. Mother_Doc 结构
- `Mother_Doc/` 当前入口形态以同名容器目录为主，不保留 `01-07` 这类编号治理目录。
- `Mother_Doc/README.md` 是镜像根说明。
- `Mother_Doc/Mother_Doc/` 是 `Octopus_OS/Mother_Doc/` 容器的自描述目录。
- `Mother_Doc/Mother_Doc/00_INDEX.md` 是 `Mother_Doc` 容器自己的索引入口。
- `Octopus_OS/<Container_Name>/` 与 `Octopus_OS/Mother_Doc/<Container_Name>/` 必须保持同名。

## 3. 动态扩容
- AI 必须依据用户描述判断是否需要横向新增容器目录。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，必须同步新增：
  - `Octopus_OS/<Container_Name>/`
  - `Octopus_OS/Mother_Doc/<Container_Name>/`
- `Mother_Doc` 本身是特例：
  - 工作目录容器为 `Octopus_OS/Mother_Doc/`
  - 自描述文档目录为 `Octopus_OS/Mother_Doc/Mother_Doc/`

## 4. 抽象层协议
- 每个容器文档目录必须先固定为：`README.md + common/`。
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

## 5. 命名约束
- 第一阶段命名规范采用“一个目录 = 一个可独立部署或独立演进的单元”。
- 第一阶段优先使用：
  - `_UI`
  - `_Gateway`
  - `_Service`
  - `_DB`
  - `_Cache`
  - `_Broker`
  - `_Storage`
- 第一阶段避免使用：
  - `Shared_*`
  - `Business_*`
  - `Runtime_*`

## 6. 第一阶段工具
- `Cli_Toolbox.materialize_container_layout`
  - 用途：依据 AI 已判定的容器名，生成 `Octopus_OS/<Container_Name>/` 与 `Octopus_OS/Mother_Doc/<Container_Name>/` 的同名目录结构，并补齐容器族对应的 `common/` 抽象层骨架。
  - 边界：工具负责落结构，不负责替 AI 做项目语义判断。
