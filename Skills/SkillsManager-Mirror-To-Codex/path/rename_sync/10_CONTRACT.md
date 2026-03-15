---
doc_id: skillsmanager_mirror_to_codex.path.rename_sync.contract
doc_type: contract_doc
topic: Rename sync contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: Rename sync requires explicit command shape.
---

# Rename 同步合同

## 当前动作的目标
- 为技能重命名提供单义同步入口，避免 codex 安装目录同时保留新旧两个文件夹。

## 当前动作必须满足的约束
- `rename` 不参与 `auto` 模式推断。
- `rename` 只接受 `scope=skill`。
- 必须同时提供：
  - `--skill-name <new_name>`
  - `--rename-from <old_name>`
- 旧名与新名不得相同。
- 如果 codex 中旧名和新名都不存在，应停止并要求改走 `push/install`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
