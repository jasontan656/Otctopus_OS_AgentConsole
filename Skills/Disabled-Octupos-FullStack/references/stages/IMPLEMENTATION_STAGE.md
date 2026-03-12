# Implementation Stage

适用阶段：`implementation`

## Scope

- 像独立人类开发者一样推进实现、测试、bring-up 与交付。
- 同步修复 `Mother_Doc` 与实际代码库/运行时之间的 drift。
- 本阶段只负责根据文档差异推进代码与运行时对齐，不负责日志与 Git / GitHub 留痕。

## Required Workflow

1. 显式承接 `mother_doc` 当前状态产物，并继续保留项目统一目标基线。
2. 先读取匹配的域族规则，再读取目标容器自己的 `common/code_abstractions/`、`common/dev_canon/` 与必要的 `common/writing_guides/` 文档。
3. 读取代码库、运行时与当前文档结构，发现 doc-code drift。
4. 先对齐文档与代码的当前状态，再继续实施。
5. 在本地可控范围内主动安装依赖、修复环境、运行测试、bring-up、验证行为。
6. `implementation` 消费 `modified` 状态范围，但不在本阶段把它改成 `developed`。
7. 把本轮完成的对齐范围、文档路径、代码路径整理成后续 `evidence` 可直接追加日志与回写 `developed` 的输入。
8. 只有本地可解动作全部穷尽后，才允许进入真实 blocked。

## Produces

- 代码改动
- 运行时改动
- 修复后的 doc-code 对齐范围
- evidence 可消费的 implementation diff 范围
- `evidence` 阶段输入
