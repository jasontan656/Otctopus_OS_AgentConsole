---
doc_id: skillsmanager_mirror_to_codex.path.rename_sync.execution
doc_type: execution_doc
topic: Rename sync execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that old and new folders no longer coexist.
---

# Rename 同步实施

## 执行顺序
1. 在真正修改前盘清 rename 影响面。
2. 使用 mirror 侧的新名字目录作为唯一源目录。
3. 先把新名字对应的 mirror 源目录覆盖到 codex 中旧名字对应的目录。
4. 覆盖完成后，把 codex 中旧名字目录重命名成新名字目录。
5. 若新名字目录已预存在 codex 中，先清理后再完成最终改名。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
