---
doc_id: skillsmanager_mirror_to_codex.path.mirror_boundary.execution
doc_type: execution_doc
topic: Mirror boundary execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that only governed roots are discovered and forbidden root files are removed.
---

# 镜像边界实施

## 执行顺序
1. 解析 codex 根与 mirror 根。
2. 锁定 skills 容器目录。
3. 发现 `.system/` 与正常技能根中的可同步根。
4. 排除产品门面、产品工具、隐藏目录与禁留项。
5. 在全量 push 后清理 codex 根禁留项。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
