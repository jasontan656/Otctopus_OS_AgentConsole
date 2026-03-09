# Doc Code Alignment Rules

适用阶段：`implementation`

## Core Rule

- `Mother_Doc` 与代码库必须保持当前状态一致。
- 发现 drift 时，默认必须更新代码追上文档；只有在新的 mother_doc 撰写明确修正文档时，才允许反向修正文档。

## Mapping Direction

- 代码架构的组织最终与 `Mother_Doc` 架构同构。
- 文档覆盖的是语义等价单元，不要求与单个代码文件机械 1:1 对齐。
- 每个模块必须有可覆盖其完整语义的文档。
- 每个模块 helper 必须有可覆盖其完整语义的 helper 文档或被上层语义文档显式收束。
- 每个父级目录与黑盒容器也必须有对应的目录实体文档。

## Status Rule

- `mother_doc` 领先于代码时，对应文档/区块必须保持 `pending_implementation`。
- 对齐完成后，implementation 必须显式把对应文档/区块改回 `aligned`。
