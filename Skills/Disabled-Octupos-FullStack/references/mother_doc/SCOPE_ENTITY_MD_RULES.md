# Scope Entity Markdown Rules

适用技能：`Disabled-Octupos-FullStack`

## Fixed Role

- 每个目录都必须有一个同名 `<folder_name>.md`。
- 该文件说明当前目录自身这个对象。

## Object Types

- 当前目录可以是：
  - 模块
  - helper 容器
  - 父级结构域
  - 黑盒容器
  - 文档承载说明层

## Maintenance Rule

- 当前目录职责、结构或边界变化后，必须同步刷新同名 `<folder_name>.md`。
- 该文件必须与未来代码组织保持对齐，因为代码架构最终与 `Mother_Doc` 架构同构。
