---
doc_id: skillsmanager_mirror_to_codex.path.push_sync.contract
doc_type: contract_doc
topic: Push sync contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: Push sync uses concrete CLI commands and rsync semantics.
---

# Push 同步合同

## 当前动作的目标
- 在目标技能已安装时，用 mirror 版本覆盖 codex 安装目录中的对应技能。
- 在 `scope=all` 时，只同步真正可同步的技能根。

## 当前动作必须满足的约束
- `push` 只做 mirror -> codex 覆盖同步，不接管安装修正。
- `scope=all` 时，只允许同步 skills 根与 `.system/`，不得把产品门面、产品工具和顶层文档直接推入 codex 安装目录。
- 同步使用 `rsync -a --delete --checksum` 语义。
- codex 根的禁留项需要在全量 push 后移除。

## 下一跳列表
- [tools]：`15_TOOLS.md`
