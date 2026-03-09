# Mother_Doc Stage

适用阶段：`mother_doc`

## Scope

- 强化当前用户意图。
- 递归读取 `Mother_Doc` 当前索引树。
- 仅在 `Mother_Doc` 树内维护 `README.md`、`agents.md`、`<folder_name>.md`、`common/` 与容器骨架。

## Required Workflow

1. 先用 `Meta-prompt-write` 强化用户意图。
2. 读取根层 `README.md`、`agents.md`、`Mother_Doc.md`。
3. 每进入下一层目录，都先读 `README.md`、再读 `agents.md`、再读同名 `<folder_name>.md`。
4. 递归选择直到完整影响面被覆盖。
5. 覆盖写回当前状态，并仅在 `Mother_Doc` 内刷新受影响目录的三类固定文件。

## Produces

- `Mother_Doc` 当前状态目录树
- 容器级文档
- 结构级索引
- `implementation` 阶段输入
