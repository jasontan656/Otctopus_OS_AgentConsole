---
doc_id: skillsmanager_mirror_to_codex.path.auto_routing.contract
doc_type: contract_doc
topic: Auto routing contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the available commands.
---

# 自动导航合同

## 当前动作的目标
- 在不丢失显式模式控制的前提下，把同步动作收敛为：
  - `push`
  - `install`
  - `rename`

## 当前动作必须满足的约束
- `scope=skill` 时必须提供 `--skill-name`。
- `--mode auto` 只在 `push` 与 `install` 之间判断，不得自动进入 `rename`。
- `--mode install` 只允许与 `--scope skill` 配合。
- `--mode rename` 必须显式提供 `--rename-from`，且不允许 `--scope all`。
- `destination_exists=true` 时，`auto` 收敛到 `push`；否则收敛到 `install`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
