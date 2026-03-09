# Implementation Stage

适用阶段：`implementation`

## Scope

- 像独立人类开发者一样推进实现、测试、bring-up 与交付。
- 同步修复 `Mother_Doc` 与实际代码库/运行时之间的 drift。
- 在每轮实现结束后追加 implementation batch 日志。

## Required Workflow

1. 显式承接 `mother_doc` 当前状态产物。
2. 读取代码库、运行时与当前文档结构，发现 doc-code drift。
3. 先对齐文档与代码的当前状态，再继续实施。
4. 在本地可控范围内主动安装依赖、修复环境、运行测试、bring-up、验证行为。
5. 把已实现范围对应的文档/区块状态从 `pending_implementation` 回写为 `aligned`。
6. 追加 implementation batch 日志。
7. 只有本地可解动作全部穷尽后，才允许进入真实 blocked。

## Produces

- 代码改动
- 运行时改动
- 修复后的 doc-code 对齐状态
- implementation batch 日志
- `evidence` 阶段输入
