---
doc_id: skillsmanager_mirror_to_codex.path.install_route.execution
doc_type: execution_doc
topic: Install route execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that install remained a route instead of a fake push.
---

# Install 路由实施

## 执行顺序
1. 确认目标技能目录当前不存在。
2. 构建 `route_required` JSON。
3. 返回后续技能顺序与下一步说明。
4. 停止当前 CLI，不在本命令内执行安装写入。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
