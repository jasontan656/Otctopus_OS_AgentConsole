# Doc Code Alignment Rules

适用阶段：`implementation`

## Core Rule

- `Mother_Doc` 与代码库必须保持当前状态一致。
- 发现 drift 时，默认必须更新代码追上文档；只有在新的 mother_doc 撰写明确修正文档时，才允许反向修正文档。

## Mapping Direction

- 代码架构的组织最终与 `Mother_Doc` 架构同构。
- 文档覆盖的是语义等价单元，不要求与单个代码文件机械 1:1 对齐。
- `overview/` 承载人类可观测总览，不直接等价单个代码文件，但必须能回指对应语义覆盖单元。
- `features/` 承载功能覆盖单元，是 implementation 对齐代码语义的主要文档入口。
- `shared/` 承载 API、event、共享合同与跨容器依赖，是 implementation 对齐容器通信与边界的主要文档入口。
- 每个模块必须有可覆盖其完整语义的文档。
- 每个模块 helper 必须有可覆盖其完整语义的 helper 文档或被上层语义文档显式收束。
- 每个父级目录与黑盒容器也必须有对应的目录实体文档。
- implementation 完成后，对齐结果必须可被 evidence 阶段回收进 `OS_graph` 的 `implementation_layer`，并保持与 `overview/features/shared` 的绑定关系。

## Status Rule

- `mother_doc` 领先于代码时，对应文档/区块必须保持 `modified`。
- `implementation` 负责消费 `modified` 状态，但不在本阶段写回 `developed`。
- 只有 `evidence` 在代码、文档、graph 与留痕闭环完成后，才把对应文档/区块改回 `developed`。
