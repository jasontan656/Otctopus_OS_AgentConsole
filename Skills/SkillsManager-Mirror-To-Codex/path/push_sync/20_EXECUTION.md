---
doc_id: skillsmanager_mirror_to_codex.path.push_sync.execution
doc_type: execution_doc
topic: Push sync execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that push covered only allowed destinations.
---

# Push 同步实施

## 执行顺序
1. 锁定源目录与目标目录。
2. 若 `scope=all`，发现 mirror 顶层真正可同步的技能根。
3. 对每个同步根执行 `rsync -a --delete --checksum`。
4. 删除 codex 根不允许保留的禁留项。
5. 返回结构化 JSON，明确同步范围与实际命令。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
