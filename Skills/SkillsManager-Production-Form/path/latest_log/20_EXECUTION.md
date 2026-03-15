---
doc_id: skillsmanager_production_form.path.latest_log.policy
doc_type: execution_doc
topic: Active log policy
reading_chain:
- key: seed_snapshot
  target: 25_LOG_SEED.md
  hop: next
  reason: After the active log policy, read the seed snapshot.
---

# Active Runtime Log 策略

## 当前 active sink
- `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`

## 当前迁移规则
- 当 governed runtime log 不存在时，先从 seed snapshot 复制初始化。
- 初始化后，新的日志写入只能留在 runtime root。
- `latest-log` 默认读取 runtime root 下的 active log。

## 下一跳列表
- [seed_snapshot]：`25_LOG_SEED.md`
