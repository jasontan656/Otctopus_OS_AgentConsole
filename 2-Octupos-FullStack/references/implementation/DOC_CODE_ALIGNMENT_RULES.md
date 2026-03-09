# Doc Code Alignment Rules

适用阶段：`implementation`

## Core Rule

- `Mother_Doc` 与代码库必须保持当前状态一致。
- 发现 drift 时，必须显式更新代码、文档或两者。

## Mapping Direction

- 代码架构的组织最终与 `Mother_Doc` 架构同构。
- 每个模块 = 一个文档。
- 每个模块 helper = 一个 helper 文档。
- 每个父级目录与黑盒容器也必须有对应的目录实体文档。

## Status Rule

- `mother_doc` 领先于代码时，对应文档/区块必须保持 `pending_implementation`。
- 对齐完成后，implementation 必须显式把对应文档/区块改回 `aligned`。
